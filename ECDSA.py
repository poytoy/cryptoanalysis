from ecpy.curves import Curve
from Crypto.Hash import SHA3_256
import random

curve = Curve.get_curve('secp256k1') #set up the curve

def KeyGen(curve): #key generation
    """Generates a public-private key pair using the secp256k1 curve."""
    private_key = random.randint(2, curve.order - 1) #get rand private key
    public_key = private_key * curve.generator #generate public key w curve
    return private_key, public_key

def SignGen(message, curve, private_key):
    """Generates a signature for a message using ECDSA.
    Args:
        message (bytes): The message to sign.
        curve: The elliptic curve used.
        private_key (int): The private key.
    Returns:
        tuple: The signature (s, h).
    """
    k = random.randint(1, curve.order - 1)
    R = k * curve.generator
    r = R.x % curve.order
    h = int(SHA3_256.new(message + r.to_bytes((r.bit_length() + 7) // 8, 'big')).hexdigest(), 16) % curve.order
    s = (k - private_key * h) % curve.order

    return s, h

def SignVer(message, s, h, curve, public_key):
    """Verifies an ECDSA signature.
    Args:
        message (bytes): The message to verify.
        s (int): Signature component s.
        h (int): Signature component h.
        curve: The elliptic curve used.
        public_key: The public key.
    Returns:
        int: 0 if the signature is valid, 1 otherwise.
    """
    V= s * curve.generator + h * public_key
    v = V.x % curve.order
    h_prime = int(SHA3_256.new(message + v.to_bytes((v.bit_length() + 7) // 8, 'big')).hexdigest(), 16) % curve.order
    return 0 if h_prime == h else 1
