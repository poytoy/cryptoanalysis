from ecpy.curves import Curve, Point
from ecpy.keys import ECPublicKey, ECPrivateKey
import hashlib
import random
import hashlib

def AddBlock2Chain(PoWLen, TxCnt, block_candidate, PrevBlock):
    #determine the previous PoW form the last block in the chain
    if not PrevBlock: #if first block
        PrevPoW = "00000000000000000000"
    else:
        PrevPoW = PrevBlock[0].strip().split(":")[1].strip()


    #read transactions from the block candidate
    transactions = "".join(block_candidate)

    '''target_prefix = '0' * PoWLen
    nonce = 0

    #perform proof of work
    while True:
        # Convert nonce to bytes
        nonce_bytes = nonce.to_bytes((nonce.bit_length() + 7) // 8, byteorder="big")
        # Combine data for hashing
        data = transactions.encode("utf-8") + nonce_bytes
        # Compute the hash
        hash_value = hashlib.sha3_256(data.encode('utf-8')).hexdigest()
        # Check if it meets the target
        if hash_value.startswith(target_prefix):
            break
        nonce += 1'''

    nonce = PoW(PoWLen, transactions, PrevPoW)

    NewBlock = f"Previous PoW: {PrevPoW}\n" + f"Nonce: {nonce}\n" + transactions
    NewPow = hashlib.sha3_256((f"{PrevPoW}{transactions}{nonce}").encode('utf-8')).hexdigest()
    return NewBlock, NewPow


'''our functions from phase II's PoW.py'''

def sha3_256(data): #computes the SHA3-256 hash of a given string
    return hashlib.sha3_256(data.encode('utf-8')).hexdigest()

def merkle_root(transactions: list) -> str:
    hashes = [sha3_256(tx) for tx in transactions] #hash each transaction
    
    while len(hashes) > 1: #combine hashes pair by pair until one hash remains (Merkle root)
        new_hashes = []

        for i in range(0, len(hashes), 2):
            if i + 1 < len(hashes):
                combined = hashes[i] + hashes[i + 1]
            else:
                combined = hashes[i] + hashes[i] #if odd number of hashes, duplicate the last one
            new_hashes.append(sha3_256(combined))
        hashes = new_hashes
    
    return hashes[0] #the remaining hash is the Merkle root

def PoW(pow_len, transactions, PrevPoW):
    #finds a valid random nonce such that SHA3-256(Hr || nonce) starts with `pow_len` zeros.
 
    root = hashlib.sha3_256((transactions + PrevPoW).encode('utf-8')).hexdigest() #compute the merkle root
    root = root.encode('utf-8')

    target_prefix = '0' * pow_len  
    nonce = 0

    while True:
        nonce_b = nonce.to_bytes(32, byteorder='big')
        data = root + nonce_b
        
        hash_value = hashlib.sha3_256(data).hexdigest() #compute the SHA3-256 hash
        if hash_value.startswith(target_prefix):
            return nonce

        nonce += 1