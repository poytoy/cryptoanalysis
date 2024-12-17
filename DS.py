import random
import gmpy2
import hashlib
import os
#import PhaseI_Test
import string


def random_string(length):
        """
        Generate a random string of the specified length.
        The string consists of uppercase, lowercase, and digits.
        """
        characters = string.ascii_letters + string.digits  # You can add more characters if needed
        return ''.join(random.choice(characters) for _ in range(length))
def generate_composite_with_exact_bit_length(num_factors, bit_length):
    """
    Generate a composite number with known factors, ensuring the composite number 
    has the exact bit length.

    Args:
        num_factors (int): Number of prime factors to use.
        bit_length (int): Desired exact bit length of the composite number.

    Returns:
        tuple: The composite number and its prime factors.
    """
    primes = []
    composite = 1

    # Generate primes and multiply them to create a composite
    while True:
        # Generate a random prime of approximately bit_length // num_factors bits
        prime_bit_length = bit_length // num_factors
        prime = generate_n_bit_prime(prime_bit_length)
        primes.append(prime)
        composite *= prime
        
        # If composite's bit length exceeds desired size, stop generating primes
        if composite.bit_length() >= bit_length:
            break

    # Adjust the composite number if it's larger than desired
    while composite.bit_length() > bit_length:
        composite //= 2  # Dividing by 2 to scale it down (keep primes intact)

    return composite, primes
def generate_n_bit_prime(n):
    """Generate an n-bit prime number efficiently."""
    if n < 2:
        raise ValueError("Number of bits must be at least 2.")
    
    # Generate a random n-bit odd number
    while True:
        candidate = random.getrandbits(n) | (1 << (n - 1)) | 1  # Ensure n-bit and odd
        if gmpy2.is_prime(candidate):  # Check primality
            return candidate
def generate_q_and_primes(n):
    while True:
        num_factors = random.randint(2, 5)
        composite, primes= generate_composite_with_exact_bit_length(num_factors,n)
        candidate=composite+1
        if gmpy2.is_prime(candidate):
            print(f"{candidate} is prime.")
            return candidate,primes
            
def generate_q_primes_and_p(q_n,p_n):
    q,primes = generate_q_and_primes(q_n)
    for _ in range(10000000):
        k = random.getrandbits( p_n-q_n-1) | (1 << (p_n - q_n - 2))
        p=k*q+1
        if gmpy2.is_prime(p):
            return q,p,primes
def find_generator(p, q, factors_of_q):
    while True:
        g = random.randint(2, p - 2)
        for d in factors_of_q:
            if gmpy2.powmod(g, q // d, p) == 1:
                break
        else:
            # If no divisor caused g^d = 1 mod p, check if g^q mod p == 1
            if pow(g, q, p) == 1:
                return g  # Found a valid generator
    
def SignGen(message, q, p, g, alpha):
    k=random.randint(1,q-2)
    r=pow(g,k,p)
    r_bytes = r.to_bytes((r.bit_length() + 7) // 8, byteorder='big')

    concatenated = message + r_bytes
    h=hashlib.sha3_256(concatenated).hexdigest()
    h_int = int(h, 16)  # Convert hex string to integer
    h_int=h_int % q #since h = SHA3_256(m||r) mod q
    s = (k - alpha * h_int) % q
    return s,h_int
def SignVer(message,s,h,q,p,g,beta):
    # Compute v = g^s * beta^h (mod p)
    v = (pow(g, s,p) * pow(beta, h,p))%p
    # Compute u = SHA3-256(m || v) (mod q)
    v_bytes = v.to_bytes((v.bit_length() + 7) // 8, byteorder='big')
  
    concatenated = message + v_bytes
    u = hashlib.sha3_256(concatenated).hexdigest()
    u_int=int(u,16)
    u_int=u_int%q
    if u_int == h:
        print("Signature is valid!")
    else:
        print("Signature is invalid!")  
def GenerateOrRead(filename):
    """
    Reads q, p, g from `filename` if it exists, otherwise generates and writes them to the file.

    Args:
        filename (str): Path to the file to read/write public parameters.

    Returns:
        tuple: The public parameters (q, p, g).
    """
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            q = int(lines[0].strip())
            p = int(lines[1].strip())
            g = int(lines[2].strip())
            return q, p, g
    else:
        q,p,primes = generate_q_primes_and_p(224,2048)
        g = find_generator(q,p,primes)
        with open(filename, 'w') as file:
            file.write(f"{q}\n")
            file.write(f"{p}\n")
            file.write(f"{g}\n")
        return q, p, g

def main():
    q,p,g=GenerateOrRead("pubparams.txt")
    print(g)
    alpha = int(input(f"chose random int between 0 and {q-1}:"))
    beta = pow(g, alpha, p)
    message=b"hello world"
    s,h = SignGen(message,q,p,g,alpha)

    SignVer(message,s,h,q,p,g,beta)
    #publish q,p,beta,g
    #private user_input
    #tests,
    #1PhaseI_Test.checkDSparams(q,p,g)
    
   
if __name__ =="__main__":
    main()