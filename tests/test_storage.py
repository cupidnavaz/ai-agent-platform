"""Storage tests."""

import unittest

from app.storage import SessionRecord


class TestStorage(unittest.TestCase):

    def test_session_record(self):

        session = SessionRecord(
            title="Test Session",
        )

        self.assertEqual(
            session.title,
            "Test Session",
        )

        self.assertIsNotNone(
            session.id,
        )


if __name__ == "__main__":
    unittest.main()
