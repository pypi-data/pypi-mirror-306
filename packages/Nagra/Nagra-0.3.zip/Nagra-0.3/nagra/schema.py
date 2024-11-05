from itertools import chain, groupby
from contextlib import contextmanager
from collections import defaultdict
from jinja2 import Template
from pathlib import Path
from io import IOBase
from typing import Optional, TYPE_CHECKING

import toml
from nagra.statement import Statement
from nagra.transaction import Transaction
from nagra.utils import logger

if TYPE_CHECKING:
    from nagra.table import Table


D2_TPL = """
{{table.name}}_: "{{table.name}}" {
  shape: sql_table
  {%- for name, col in table.columns.items() %}
  {{name}}: {{col.dtype}}
  {%- endfor %}
}
{%- for col, ftable in table.foreign_keys.items() %}
{{table.name}}_.{{col}} -> {{ftable}}_.id : "{{col}}"
{%- endfor -%}
"""


class Schema:
    _default = None

    def __init__(self, tables=None):
        self.tables = tables or {}

    @classmethod
    @property
    def default(cls):
        if not cls._default:
            cls._default = Schema()
        return cls._default

    @classmethod
    def from_toml(self, toml_src: IOBase | Path | str) -> "Schema":
        schema = Schema()
        schema.load_toml(toml_src)
        return schema

    def load_toml(self, toml_src: IOBase | Path | str):
        # Late import to avoid import loops
        from nagra.table import Table

        # load table definitions
        match toml_src:
            case IOBase():
                content = toml_src.read()
            case Path():
                content = toml_src.open().read()
            case _:
                content = toml_src
        tables = toml.loads(content)
        # Instanciate tables
        for name, info in tables.items():
            logger.debug("Instanciate %s from toml", name)
            Table(name, **info, schema=self)

    def add(self, name: str, table: "Table"):
        if name in self.tables:
            raise RuntimeError(f"Table {name} already in schema!")
        self.tables[name] = table

    def reset(self):
        self.tables = {}

    def get(self, name: str) -> "Table":
        """
        Return the table with name `name`
        """
        return self.tables[name]

    @classmethod
    def _db_columns(cls, trn=None, pg_schema="public"):
        from nagra.table import _TYPE_ALIAS

        trn = trn or Transaction.current
        res = defaultdict(dict)
        stmt = Statement("find_columns", trn.flavor, pg_schema=pg_schema)
        for tbl, col_name, col_type, *hints in trn.execute(stmt()):
            if col_type.upper() == "ARRAY" and hints:
                # Try to find type of elements, rely on the fact that
                # _TYPE_ALIAS keys are sorted by reverse length.
                hint = hints[0].lower()
                for candidate in _TYPE_ALIAS:
                    if candidate in hint:
                        # XXX We can not detect array dimensions,
                        # fallback to simple array
                        col_type = f"{candidate} []"
                        break
                else:
                    msg = f"Unable to detect type of column: {col_name} in table {tbl}"
                    raise RuntimeError(msg)
            res[tbl][col_name] = col_type
        return res

    @classmethod
    def _db_fk(cls, *whitelist, trn=None, pg_schema="public"):
        trn = trn or Transaction.current
        res = defaultdict(dict)
        stmt = Statement("find_foreign_keys", trn.flavor, pg_schema=pg_schema)
        for name, tbl, col, ftable, fcol in trn.execute(stmt()):
            if whitelist and tbl not in whitelist:
                continue
            if name in res[tbl]:
                raise RuntimeError("Unexpected multi-columns foreign key")
            res[tbl][name] = FKConstraint(name, tbl, col, ftable, fcol)
        return res

    @classmethod
    def _db_pk(cls, trn=None, pg_schema="public"):
        trn = trn or Transaction.current
        res = {}
        stmt = Statement("find_primary_keys", trn.flavor, pg_schema=pg_schema)
        for tbl, pk_col in trn.execute(stmt()):
            if tbl in res:
                raise RuntimeError("Unexpected multi-columns primary key")
            res[tbl] = pk_col
        return res

    @classmethod
    def _db_unique(cls, trn=None, pg_schema="public"):
        trn = trn or Transaction.current
        by_constraint = defaultdict(list)

        if trn.flavor == "sqlite":
            stmt = Statement("find_unique_constraint", trn.flavor)
            constraints = trn.execute(stmt()).fetchall()
            for (tbl, idx_name), rows in groupby(constraints, key=lambda x: x[:2]):
                rows = list(rows)
                by_constraint[tbl].append([col_name for _, _, col_name in rows])

        else:
            stmt = Statement("find_unique_constraint", trn.flavor, pg_schema=pg_schema)
            constraints = trn.execute(stmt()).fetchall()
            for tbl, constraint_name in constraints:
                col_stmt = Statement(
                    "find_index_columns",
                    trn.flavor,
                    pg_schema=pg_schema,
                    name=constraint_name,
                )
                columns = [c for c, in trn.execute(col_stmt())]
                by_constraint[tbl].append(columns)

        # Keep the unique constraint with the lowest number of columns for
        # each table
        res = {}
        for table, constraints in by_constraint.items():
            first, *_ = sorted(constraints, key=lambda item: len(item))
            res[table] = first
        return res

    def setup_statements(self, trn=None):
        trn = trn or Transaction.current

        # Find existing tables and columns
        db_columns = self._db_columns(trn)

        # Create tables
        for name, table in self.tables.items():
            if name in db_columns:
                continue
            ctypes = table.ctypes(trn.flavor, table.columns)
            # TODO use KEY GENERATED ALWAYS AS IDENTITY) instead of
            # serials (see https://stackoverflow.com/a/55300741) ?
            stmt = Statement(
                "create_table",
                trn.flavor,
                table=table,
                pk_type=ctypes.get(table.primary_key),
            )
            yield stmt()

        # Add columns
        for table in self.tables.values():
            ctypes = table.ctypes(trn.flavor, table.columns)
            for column in table.columns:
                if column == table.primary_key:
                    continue
                if column in db_columns.get(table.name, []):
                    continue
                stmt = Statement(
                    "add_column",
                    flavor=trn.flavor,
                    table=table.name,
                    column=column,
                    col_def=ctypes[column],
                    not_null=column in table.not_null,
                    fk_table=table.foreign_keys.get(column),
                    default=table.default.get(column),
                )
                yield stmt()

        # Add index on natural keys
        for name, table in self.tables.items():
            stmt = Statement(
                "create_unique_index",
                trn.flavor,
                table=name,
                natural_key=table.natural_key,
            )
            yield stmt()

    def create_tables(self, trn=None):
        """
        Create tables, indexes and foreign keys
        """
        trn = trn or Transaction.current
        # Loop on setup statements and execute them
        for stm in self.setup_statements(trn=trn):
            trn.execute(stm)

    @classmethod
    def from_db(cls, trn: Optional[Transaction] = None) -> "Schema":
        """ "
        Instanciate a nagra Schema (and Tables) based on database
        schema
        """
        trn = trn or Transaction.current
        schema = Schema()
        schema.introspect_db(trn=trn)
        return schema

    def introspect_db(self, *tables: str, trn: Optional[Transaction] = None):
        """
        Instanciate Table instances based on database content. If
        `tables` is non-empty, it is used as a whitelist and all other
        tables are ignored
        """
        from nagra.table import Table, UNSET

        trn = trn or Transaction.current
        db_fk = self._db_fk(*tables, trn=trn)
        db_pk = self._db_pk(trn=trn)
        db_unique = self._db_unique(trn=trn)
        db_columns = self._db_columns(trn=trn)

        for table_name, cols in db_columns.items():
            if tables and table_name not in tables:
                continue
            fks = {fk.column: fk.foreign_table for fk in db_fk[table_name].values()}
            # Instanciate table
            Table(
                table_name,
                columns=cols,
                natural_key=db_unique.get(table_name),
                foreign_keys=fks,
                primary_key=db_pk.get(table_name, UNSET),
                schema=self,
            )

    def drop(self, trn=None):
        trn = trn or Transaction.current
        for table in self.tables.values():
            table.drop(trn)

    def generate_d2(self):
        tpl = Template(D2_TPL)
        tables = self.tables.values()
        res = "\n".join(tpl.render(table=t) for t in tables)
        return res

    @contextmanager
    def suspend_fk(self, trn: Optional[Transaction] = None):
        """
        Temporarily drop all foreign keys and re-add them when
        exiting.  The db is introspected each time `suspend_fk` is
        called and the content of Schema is ignored, so the code may drop
        and re-add more foreign keys.
        """
        msg = "suspend_fk is only supported with Postgresql"
        assert Transaction.current.flavor == "postgresql", msg

        all_fks = list(
            chain.from_iterable(fks.values() for fks in self._db_fk(trn=trn).values())
        )
        for fk in all_fks:
            fk.drop()
        yield

        for fk in all_fks:
            fk.add()


class FKConstraint:
    def __init__(self, name, table, column, foreign_table, foreign_column):
        self.name = name
        self.table = table
        self.column = column
        self.foreign_table = foreign_table
        self.foreign_column = foreign_column

    def drop(self, trn=None):
        trn = trn or Transaction.current
        stmt = Statement(
            "drop_fk",
            trn.flavor,
            table=self.table,
            name=self.name,
        )
        trn.execute(stmt())

    def add(self, trn=None):
        trn = trn or Transaction.current
        stmt = Statement(
            "add_foreign_key",
            trn.flavor,
            table=self.table,
            column=self.column,
            name=self.name,
            foreign_table=self.foreign_table,
            foreign_column=self.foreign_column,
        )
        trn.execute(stmt())
