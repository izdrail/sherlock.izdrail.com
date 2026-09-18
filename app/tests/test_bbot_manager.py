import asyncio
import sys
from types import ModuleType

fake_bbot = ModuleType("bbot")
fake_scanner_module = ModuleType("bbot.scanner")
fake_scanner_module.Scanner = object
sys.modules.setdefault("bbot", fake_bbot)
sys.modules.setdefault("bbot.scanner", fake_scanner_module)
import unittest
from unittest.mock import patch

from services.bbot_manager import BBotManager


class FakeEvent:
    def json(self): return {"type": "DNS_NAME", "data": "example.com"}


class FakeScanner:
    status = "NOT_STARTED"
    stopped = False
    def __init__(self, *args, **kwargs): self.status = "STARTING"
    async def async_start(self):
        self.status = "RUNNING"
        yield FakeEvent()
        self.status = "FINISHED"
    async def stop(self): self.status = "ABORTED"; self.stopped = True


class BBotManagerTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self): BBotManager._scans.clear()

    @patch("services.bbot_manager.Scanner", FakeScanner)
    async def test_runs_and_collects_events(self):
        created = await BBotManager.start("example.com")
        await BBotManager._scans[created["id"]].task
        self.assertEqual(BBotManager.get(created["id"]).status, "FINISHED")
        self.assertEqual(BBotManager.events(created["id"])["events"][0]["type"], "DNS_NAME")

    async def test_lists_allowed_presets(self):
        self.assertIn("subdomain-enum", BBotManager.ALLOWED_PRESETS)


if __name__ == "__main__": unittest.main()
