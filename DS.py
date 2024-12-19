import random
import gmpy2
import hashlib
import os
import string

#1.Setup for public parameter generation
def random_string(length):
    #generates a random string of the specified length, with uppercase, lowercase, and digits.
    characters = string.ascii_letters + string.digits  # You can add more characters if needed
    return ''.join(random.choice(characters) for _ in range(length))

def generate_n_bit_prime(n):
    if n < 2:
        raise ValueError("Number of bits must be at least 2.")
    
    # Generate a random n-bit odd number
    while True:
        candidate = random.getrandbits(n) | (1 << (n - 1)) | 1  # Ensure n-bit and odd
        if gmpy2.is_prime(candidate):  # Check primality
            return candidate

def generate_q_and_p(q_n,p_n):
    q = generate_n_bit_prime(q_n)

    for _ in range(10000000):
        k = random.getrandbits( p_n - q_n - 1) | (2 << (p_n - q_n - 2))
        p=k*q+1
        if(p.bit_length()==p_n):#check p.bit_length() == p_n
            if gmpy2.is_prime(p): #check p is prime
                print("bit size of q: ", q.bit_length())
                print("bit size of p: ", p.bit_length())
                return q,p,k

def find_generator(p,q,k):
    g = 1 #initialize g

    while g == 1: #loop until valid generator is found
        alpha = random.randint(2, p - 1) #random seed
        g = pow(alpha, k, p) #candidate generator

    return g

#2.Key Generation
def KeyGen(q,p,g):
    alpha = int(input(f"Choose random int between 0 and {q-1}: "))
    beta = pow(g, alpha, p)
    return alpha, beta

#3.Signature Generation
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

#4.Signature Verification
def SignVer(message,s,h,q,p,g,beta):
    # Compute v = g^s * beta^h (mod p)
    v = (pow(g, s,p) * pow(beta, h,p))%p
    # Compute u = SHA3-256(m || v) (mod q)
    v_bytes = v.to_bytes((v.bit_length() + 7) // 8, byteorder='big')
  
    concatenated = message + v_bytes
    u = hashlib.sha3_256(concatenated).hexdigest()
    u_int = int(u,16)
    u_int = u_int%q

    if u_int == h:
        return 0
    else:
        return 1

def GenerateOrRead(filename):
    #reads q, p, g from `filename` if it exists, otherwise generates and writes them to the file.

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            q = int(lines[0].strip())
            p = int(lines[1].strip())
            g = int(lines[2].strip())
            return q, p, g
        
    else:
        q,p,k = generate_q_and_p(224,2048)#should be 224 2048
        g = find_generator(p,q,k)
        with open(filename, 'w') as file:
            file.write(f"{q}\n")
            file.write(f"{p}\n")
            file.write(f"{g}\n")
        return q, p, g
