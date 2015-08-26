from metahosting.common import get_uuid
from unittest import TestCase


class TestCommon(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_uuid(self):
        filename = 'tests/files/uuid.txt'
        uuid = get_uuid(filename)
        self.assertIs(str, type(uuid))

    def test_get_uuid_wrong_path(self):
        filename = 'wrong/path'
        uuid = get_uuid(filename)
        self.assertIs(str, type(uuid))

    def test_get_uuid_wrong_content(self):
        filename = 'tests/files/uuid_wrong.txt'
        uuid = get_uuid(filename)
        self.assertIs(str, type(uuid))
