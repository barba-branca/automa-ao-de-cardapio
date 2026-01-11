import os
import pytest
import database as db

# Use a temporary database for testing
TEST_DB = "test_saka.db"

@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup: Override the DB path in the module
    original_db_path = db.DB_PATH
    db.DB_PATH = db.Path(TEST_DB)

    # Initialize DB
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    db.init_db()

    yield

    # Teardown: Remove the test database
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    db.DB_PATH = original_db_path

def test_create_order():
    order_id = db.create_order("ifood", "John Doe", "1x Burger")
    assert order_id is not None

    order = db.get_order_by_id(order_id)
    assert order['client_name'] == "John Doe"
    assert order['status'] == db.STATUS_NOVO

def test_update_status():
    order_id = db.create_order("ifood", "Jane Doe", "1x Salad")
    assert db.update_order_status(order_id, db.STATUS_PREPARANDO)

    order = db.get_order_by_id(order_id)
    assert order['status'] == db.STATUS_PREPARANDO

def test_delete_order():
    order_id = db.create_order("ifood", "To Delete", "1x Water")
    assert db.delete_order(order_id)
    assert db.get_order_by_id(order_id) is None

def test_get_all_orders():
    db.create_order("ifood", "Client 1", "Item 1")
    db.create_order("99food", "Client 2", "Item 2")

    orders = db.get_all_orders()
    assert len(orders) == 2

def test_get_orders_count():
    db.create_order("ifood", "Client 1", "Item 1") # Novo
    id2 = db.create_order("ifood", "Client 2", "Item 2")
    db.update_order_status(id2, db.STATUS_PREPARANDO)

    counts = db.get_orders_count_by_status()
    assert counts[db.STATUS_NOVO] == 1
    assert counts[db.STATUS_PREPARANDO] == 1
