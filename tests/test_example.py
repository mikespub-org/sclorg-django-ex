from tests import BaseTestCase


class IndexTest(BaseTestCase):
    """
    Test that index is accessible
    """

    def test_index(self):
        with self.client:
            result = self.client.get("/")
            expected_content = "Hello World"
            self.assertIn(expected_content, str(result.data))
            self.assertEqual(result.status_code, 200)
