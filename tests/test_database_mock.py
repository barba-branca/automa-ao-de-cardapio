import unittest
from unittest.mock import MagicMock, patch
import database as db

class TestDatabasePostgres(unittest.TestCase):

    @patch('database.psycopg2.connect')
    def test_create_order(self, mock_connect):
        # Mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # Mock returning ID
        mock_cursor.fetchone.return_value = [1]

        # Call function
        order_id = db.create_order("ifood", "John Doe", "1x Burger")

        # Verify
        self.assertEqual(order_id, 1)
        # Verify SQL contains %s
        args, _ = mock_cursor.execute.call_args
        sql = args[0]
        self.assertIn("%s", sql)
        self.assertIn("INSERT INTO orders", sql)

        # Verify commit called
        mock_conn.commit.assert_called()

    @patch('database.psycopg2.connect')
    def test_get_all_orders(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # Mock rows
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'source': 'ifood', 'status': 'novo'},
            {'id': 2, 'source': 'whatsapp', 'status': 'preparando'}
        ]

        orders = db.get_all_orders()

        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0]['id'], 1)

    @patch('database.psycopg2.connect')
    def test_update_status(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.rowcount = 1

        success = db.update_order_status(1, db.STATUS_PREPARANDO)

        self.assertTrue(success)
        mock_cursor.execute.assert_called()
        args, _ = mock_cursor.execute.call_args
        sql = args[0]
        self.assertIn("UPDATE orders", sql)
        self.assertIn("%s", sql)

    @patch('database.psycopg2.connect')
    def test_clear_old_orders(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_cursor.rowcount = 5

        deleted = db.clear_old_orders(24)

        self.assertEqual(deleted, 5)
        args, _ = mock_cursor.execute.call_args
        sql = args[0]
        # Check for postgres specific interval syntax
        self.assertIn("INTERVAL '1 hour' * %s", sql)

if __name__ == '__main__':
    unittest.main()
