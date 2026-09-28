from dht import calculate_hash, is_prime, next_prime


def test_prime_helpers():
    assert not is_prime(1)
    assert is_prime(211)
    assert next_prime(200) == 211


def test_hash():
    assert calculate_hash(383097, 211, 3) == (132, 0)
