import unittest
import tempfile
import os
from pathlib import Path
import database
import app as app_module


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database.DB_PATH = Path(self.temp_dir.name) / "test_expenses.db"
        database.init_db()
        app_module.app.config["TESTING"] = True
        self.client = app_module.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_expenses_empty(self):
        response = self.client.get("/api/expenses")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_add_expense(self):
        response = self.client.post("/api/expenses", json={
            "amount": 120, "category": "Продукты",
            "date": "2026-07-02", "comment": "Тест"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["category"], "Продукты")

    def test_reject_negative_amount(self):
        response = self.client.post("/api/expenses", json={
            "amount": -5, "category": "Другое", "date": "2026-07-02"
        })
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
