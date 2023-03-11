import pytest
import sqlite3
import os
from typing import List, Dict, Any, Union
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category


@pytest.fixture(scope="function")
def db_file() -> str:
    db_file = 'test.db'
    yield db_file
    os.remove(db_file)


@pytest.fixture
def repo(db_file: str) -> SQLiteRepository[Category]:
    return SQLiteRepository[Category](db_file, Category)


@pytest.fixture
def category1() -> Category:
    return Category(name="продукты", parent=None, pk=1)


@pytest.fixture
def category2() -> Category:
    return Category(name="мясо", parent=1, pk=2)



def test_add(repo: SQLiteRepository[Category], category1: Category, category2: Category) -> None:
    assert repo.add(category1) == 1
    assert repo.add(category2) == 2


def test_get(repo: SQLiteRepository[Category], category1: Category, category2: Category) -> None:
    repo.add(category1)
    repo.add(category2)
    assert repo.get(1) == category1
    assert repo.get(2) == category2
    assert repo.get(3) is None


def test_get_all(repo: SQLiteRepository[Category], category1: Category, category2: Category) -> None:
    assert repo.get_all() == []
    repo.add(category1)
    repo.add(category2)
    assert repo.get_all() == [category1, category2]
    assert repo.get_all(where={"name": "продукты"}) == [category1]


def test_update(repo: SQLiteRepository[Category], category1: Category, category2: Category) -> None:
    repo.add(category1)
    repo.add(category2)
    new_category = Category(name="книги", parent=None, pk=1)
    repo.update(new_category)
    assert repo.get(1) == category1


def test_delete(repo: SQLiteRepository[Category], category1: Category, category2: Category) -> None:
    repo.add(category1)
    repo.add(category2)
    repo.delete(1)
    assert repo.get_all() == [category2]
    