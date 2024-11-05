from pathlib import Path

import pytest

from nagra import Table, Schema
from nagra.table import Column
from nagra.exceptions import IncorrectTable


HERE = Path(__file__).parent


def test_toml_loader():

    # With a Path
    src = HERE / "assets" / "sample_schema.toml"
    test_schema = Schema.from_toml(src)
    table = Table.get("user", schema=test_schema)
    assert table is not None

    # with a string
    test_schema = Schema.from_toml(src.open().read())
    table = Table.get("user", schema=test_schema)
    assert table is not None

    # with an io base
    test_schema = Schema.from_toml(src.open())
    table = Table.get("user", schema=test_schema)
    assert table is not None

    # Must fail when a duplicate table is added
    with pytest.raises(RuntimeError):
        Table(
            "user",
            columns={"name": "varchar"},
            natural_key=["name"],
            schema=test_schema,
        )

    # Test reset
    test_schema.reset()
    assert test_schema.tables == {}


def test_setup():
    pass  # TODO test generated sql


def test_bogus_fk(empty_transaction):
    with pytest.raises(IncorrectTable):
        Table(
            "bogus",
            columns={
                "key": "uuid",
            },
            natural_key=["key"],
            foreign_keys={
                "key": "bogus",
            },
        )


def test_create_tables(empty_transaction):
    # Associate schema with the transaction
    schema = Schema.default

    # Make sure we start from empty db
    assert not schema._db_columns(trn=empty_transaction)
    schema.create_tables(trn=empty_transaction)
    post = schema._db_columns(trn=empty_transaction)

    # Test person table is properly created
    assert "person" in post
    assert sorted(post["person"]) == ["id", "name", "parent"]

    # Add a column to existing table
    person = Table.get("person")
    person.columns["email"] = Column("email", "varchar")
    schema.create_tables(trn=empty_transaction)
    post = schema._db_columns(trn=empty_transaction)
    assert "person" in post
    assert sorted(post["person"]) == ["email", "id", "name", "parent"]

    # Needed to not polute other tests
    person.columns.pop("email")


def test_custom_id_type(empty_transaction):
    sch = Schema()
    city = Table(
        "city",
        columns={
            "id": "varchar",  # XXX it's prob better to not put id in columns
            "name": "varchar",
        },
        schema=sch,
    )
    with empty_transaction:
        sch.drop()
        sch.create_tables()
        row_id = city.upsert("id", "name").execute("this-is-an-uuid", "test")
        assert row_id == "this-is-an-uuid"
        assert list(city.select()) == [("this-is-an-uuid", "test")]


def test_schema_from_db(transaction):
    schema = Schema()
    tables = [
        "address",
        "country",
        "kitchensink",
        "org",
        "parameter",
        "person",
        "skill",
        "temperature",
    ]
    schema.introspect_db()
    assert sorted(schema.tables) == tables

    # Check simple table
    person = schema.get("person")
    assert list(person.columns) == ["id", "name", "parent"]
    if transaction.flavor == "postgresql":
        expected = ["bigint", "str", "int"]
    else:
        expected = ["int", "str", "int"]
    assert [c.dtype for c in person.columns.values()] == expected
    assert person.foreign_keys == {"parent": "person"}
    assert person.primary_key == "id"
    assert person.natural_key == ["name"]

    # Check table with arrays
    parameter = schema.get("parameter")
    assert list(parameter.columns) == ["id", "name", "timestamps", "values"]
    if transaction.flavor == "postgresql":
        expected_types = ["bigint", "str", "timestamp", "float"]
        assert [c.dtype for c in parameter.columns.values()] == expected_types
        expected_dims = ["", "", "[]", "[]"]
        assert [c.dims for c in parameter.columns.values()] == expected_dims
    else:
        expected_types = ["int", "str", "json", "json"]
        assert [c.dtype for c in parameter.columns.values()] == expected_types

    assert parameter.foreign_keys == {}
    assert parameter.primary_key == "id"
    assert parameter.natural_key == ["name"]


def test_suspend_fk(transaction):
    # Skip sqlite
    if transaction.flavor == "sqlite":
        return

    schema = Schema()
    whitelist = ["person", "skill"]
    schema.introspect_db(*whitelist)

    before = schema._db_fk(*whitelist)
    with schema.suspend_fk():
        with_suspend = schema._db_fk(*whitelist)
    after = schema._db_fk(*whitelist)

    assert len(with_suspend) == 0
    assert sorted(before) == ["person", "skill"]
    assert sorted(after) == ["person", "skill"]
    assert sorted(before["person"]) == ["fk_parent"]
    assert sorted(after["person"]) == ["fk_parent"]
