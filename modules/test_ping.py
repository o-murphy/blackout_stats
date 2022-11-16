import unittest
from ping import ping


class TestPing(unittest.TestCase):

    def test_ping_by_ip(self):

        with self.subTest('valid host response'):
            code, res = ping('google.com')
            self.assertTrue(code)

        with self.subTest('invalid host response'):
            code, res = ping('uihwehuifwrufha.c')
            self.assertFalse(code)

    def test_ping_by_port(self):

        with self.subTest('valid port response'):
            code, res = ping('google.com:80')
            self.assertTrue(code)

        with self.subTest('invalid port response'):
            code, res = ping('google.com:882')
            self.assertFalse(code)

        with self.subTest('invalid host response'):
            code, res = ping('uihwehuifwrufha.c:80')
            self.assertFalse(code)


if __name__ == '__main__':
    unittest.main()
