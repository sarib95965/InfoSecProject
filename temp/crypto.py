from kyber_py.kyber.default_parameters import Kyber512

# Pre-configured Kyber512 instance
kyber = Kyber512

def generate_keys():
    """
    Generates a Kyber512 key pair.
    Returns:
        tuple(bytes, bytes): (public_key, private_key)
    """
    public_key, private_key = kyber.keygen()
    return public_key, private_key


def encrypt_message(public_key_hex, message=None):
    """
    Encapsulates a shared secret using the provided public key.
    Args:
        public_key_hex (str): hex-encoded public key
        message: placeholder for future hybrid-encryption (ignored for KEM)
    Returns:
        tuple(bytes, bytes): (ciphertext, shared_secret)
    """
    public_key = bytes.fromhex(public_key_hex)
    shared_secret, ciphertext = kyber.encaps(public_key)
    return ciphertext, shared_secret


def decrypt_message(private_key_hex, ciphertext_hex):
    """
    Decapsulates the shared secret using the provided private key and ciphertext.
    Args:
        private_key_hex (str): hex-encoded private key
        ciphertext_hex (str): hex-encoded ciphertext
    Returns:
        bytes: shared_secret
    """
    private_key = bytes.fromhex(private_key_hex)
    ciphertext = bytes.fromhex(ciphertext_hex)
    shared_secret = kyber.decaps(private_key, ciphertext)
    return shared_secret
