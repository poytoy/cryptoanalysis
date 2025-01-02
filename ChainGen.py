import hashlib
from Crypto.Hash import SHA3_256

#the pdf says the arguments should be as PoWLen, TxCnt, PrevBlock, block_candidate; but i followed the order in the PhaseIII_Test.py
def AddBlock2Chain(PoWLen, TxCnt, block_candidate, PrevBlock):
    transactions = "".join(block_candidate[:TxCnt*9])
    if not PrevBlock: #if first block
        PrevPoW = "00000000000000000000"
        nonce, _ = PoW(PoWLen, transactions, PrevPoW)
    else: #determine the previous PoW form the last block in the chain
        
        nonce, PrevPoW = PoW(PoWLen, transactions, PrevBlock[0][14:])
        #PrevPoW = hashlib.sha3_256("".join(PrevBlock).encode('utf-8')).hexdigest()

    #read transactions from the block candidate
    
    NewBlock = f"Previous PoW: {PrevPoW}\n" + f"Nonce: {nonce}\n" + transactions
    return NewBlock, PrevPoW


'''our functions from phase II's PoW.py'''
def sha3_256(data):
    # Compute SHA3-256 hash and return the digest
    if isinstance(data, str):
        data = data.encode('utf-8')  # Convert string to bytes
    return SHA3_256.new(data).digest()

def merkle_root(transactions: list) -> bytes:
    # Compute initial transaction hashes
    hashTree = [SHA3_256.new(tx if isinstance(tx, bytes) else tx.encode('utf-8')).digest() for tx in transactions]
    t = len(transactions)
    j = 0

    while t > 1:
        for i in range(j, j + t, 2):
            if i + 1 < j + t:
                combined = hashTree[i] + hashTree[i + 1]
            else:
                combined = hashTree[i] + hashTree[i]  # Duplicate the last hash if odd
            hashTree.append(SHA3_256.new(combined).digest())
        j += t
        t = t >> 1  # Move to the next level

    return hashTree[2 * len(transactions) - 2]
def PoW(PowLen, transactions, PrevPoW):
    #finds a valid random nonce such that SHA3-256(Hr||prevPoW || nonce) starts with `pow_len` zeros.
 
    root = merkle_root(transactions)

    target_prefix = '0' * PowLen  
    nonce = 0

    while True:
        nonce_b = nonce.to_bytes((nonce.bit_length() + 7) // 8 or 1, byteorder='big')
        prevPoW_bytes = PrevPoW.encode('utf-8') if isinstance(PrevPoW, str) else PrevPoW
        data = root +  prevPoW_bytes + nonce_b
        
        
        hash_value = hashlib.sha3_256(data).hexdigest() #compute the SHA3-256 hash
        if hash_value.startswith(target_prefix):
            print("root: ",root)
            return nonce, hash_value
        

        nonce += 1