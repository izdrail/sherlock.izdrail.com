import unittest
from unittest.mock import Mock, patch

from fastapi import HTTPException
from services.spiderfoot_gateway import SpiderFootGateway


class SpiderFootGatewayTest(unittest.TestCase):
    def test_catalog_covers_scan_read_and_control_operations(self):
        catalog = SpiderFootGateway.catalog()
        for name in ("scanlist", "scanstatus", "scanlog", "scaneventresults", "startscan", "stopscan", "scandelete"):
            self.assertIn(name, catalog)

    @patch("services.spiderfoot_gateway.requests.get")
    def test_read_uses_query_params_and_timeout(self, get):
        response = Mock(ok=True)
        get.return_value = response
        self.assertIs(SpiderFootGateway.invoke("scanstatus", {"id": "123"}), response)
        get.assert_called_once_with(f"{SpiderFootGateway.BASE_URL}/scanstatus", params={"id": "123"}, timeout=SpiderFootGateway.TIMEOUT)

    def test_rejects_unknown_endpoints_and_parameters(self):
        with self.assertRaises(HTTPException): SpiderFootGateway.invoke("query", {"query": "select *"})
        with self.assertRaises(HTTPException): SpiderFootGateway.invoke("scanstatus", {"id": "1", "url": "https://evil.invalid"})


if __name__ == "__main__": unittest.main()
