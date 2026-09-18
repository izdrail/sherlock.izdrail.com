import unittest
from api.endpoints.security import serialize_scan

class ScanContractTest(unittest.TestCase):
    def test_serializes_spiderfoot_scan_row(self):
        row = ['id-1', 'example.com', 'device-1 case', 1, 2, 1, 'FINISHED', 10, 'LOW']
        result = serialize_scan(row)
        self.assertEqual(result['guid'], 'id-1')
        self.assertEqual(result['name'], 'device-1 case')
        self.assertEqual(result['status'], 'FINISHED')

    def test_preserves_dict_rows(self):
        row = {'guid': 'id-1', 'status': 'RUNNING'}
        self.assertIs(serialize_scan(row), row)

if __name__ == '__main__': unittest.main()
