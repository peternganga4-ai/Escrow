"""Tests for services.product_service — Product listing and display."""

from services.product_service import list_products, find_product, save_product


def test_list_products_empty(patched_db):
    result = list_products()
    assert result == []

