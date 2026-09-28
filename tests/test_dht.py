import unittest

from dht import calculate_hash, is_prime, next_prime


class DhtTests(unittest.TestCase):
    def test_prime_helpers(self):
        self.assertFalse(is_prime(1))
        self.assertTrue(is_prime(211))
        self.assertEqual(next_prime(200), 211)

    def test_hash(self):
        self.assertEqual(calculate_hash(383097, 211, 3), (132, 0))


if __name__ == "__main__":
    unittest.main()
