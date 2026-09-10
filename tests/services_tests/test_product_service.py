"""Tests for services.product_service — Product listing and display."""

from services.product_service import list_products, find_product, save_product


def test_list_products_empty(patched_db):
    result = list_products()
    assert result == []

def test_list_products_returns_all(patched_db, sample_product):
    result = list_products()
    assert len(result) == 1
    assert result[0].product_id == "P001"


def test_find_product_existing(patched_db, sample_product):
    p = find_product("P001")
    assert p is not None
    assert p.name == "Laptop"
    assert p.price == 85000



def test_find_product_not_found(patched_db):
    assert find_product("P999") is None

