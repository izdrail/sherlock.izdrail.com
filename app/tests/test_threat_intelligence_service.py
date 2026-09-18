import unittest
from unittest.mock import Mock, patch

from services.threat_intelligence_service import ThreatIntelligenceService


class ThreatIntelligenceServiceTest(unittest.TestCase):
    def setUp(self):
        ThreatIntelligenceService._cache.clear()

    @patch("services.threat_intelligence_service.requests.get")
    def test_filters_and_sorts_known_exploited(self, get):
        response = Mock()
        response.json.return_value = {"catalogVersion": "1", "vulnerabilities": [
            {"cveID": "CVE-1", "vendorProject": "Other", "dateAdded": "2026-01-01"},
            {"cveID": "CVE-2", "vendorProject": "Example", "dateAdded": "2026-02-01"},
        ]}
        response.raise_for_status.return_value = None
        get.return_value = response
        result = ThreatIntelligenceService.known_exploited(query="example")
        self.assertEqual(result["vulnerabilities"][0]["cveID"], "CVE-2")
        self.assertEqual(result["source_url"], ThreatIntelligenceService.CISA_KEV_URL)

    @patch("services.threat_intelligence_service.requests.get")
    def test_caches_identical_requests(self, get):
        response = Mock()
        response.json.return_value = {"totalResults": 0, "vulnerabilities": []}
        response.raise_for_status.return_value = None
        get.return_value = response
        ThreatIntelligenceService.recent_cves(limit=2)
        ThreatIntelligenceService.recent_cves(limit=2)
        self.assertEqual(get.call_count, 1)

    @patch("services.threat_intelligence_service.requests.get")
    def test_returns_epss_score(self, get):
        response = Mock()
        response.json.return_value = {"data": [{"cve": "CVE-2026-1234", "epss": "0.42"}]}
        response.raise_for_status.return_value = None
        get.return_value = response
        result = ThreatIntelligenceService.epss("cve-2026-1234")
        self.assertEqual(result["result"]["epss"], "0.42")


if __name__ == "__main__":
    unittest.main()
