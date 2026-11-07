import tempfile
import unittest
from pathlib import Path

from src.memory.store import MemoryStore


class MemoryStoreTests(unittest.TestCase):
    def test_saves_and_reads_messages(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = MemoryStore(str(Path(temp_dir) / "memory.sqlite3"))
            store.save("user", "Olá, Conori")
            history = store.recent()
            self.assertEqual(len(history), 1)
            self.assertEqual(history[0][0], "user")
            self.assertEqual(history[0][1], "Olá, Conori")


if __name__ == "__main__":
    unittest.main()
