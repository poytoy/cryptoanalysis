import hashlib

#the pdf says the arguments should be as PoWLen, TxCnt, PrevBlock, block_candidate; but i followed the order in the PhaseIII_Test.py
def AddBlock2Chain(PoWLen, TxCnt, block_candidate, PrevBlock):

    if not PrevBlock: #if first block
        PrevPoW = "00000000000000000000"
        nonce, _ = PoW(PoWLen, "".join(PrevBlock[2:]), PrevPoW)
    else: #determine the previous PoW form the last block in the chain
        nonce, PrevPoW = PoW(PoWLen, "".join(PrevBlock[2:]), PrevBlock[0][14:])
        #PrevPoW = hashlib.sha3_256("".join(PrevBlock).encode('utf-8')).hexdigest()

    #read transactions from the block candidate
    transactions = "".join(block_candidate[:TxCnt*9])
    NewBlock = f"Previous PoW: {PrevPoW}\n" + f"Nonce: {nonce}\n" + transactions

    return NewBlock, PrevPoW


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

def PoW(PowLen, transactions, PrevPoW):
    #finds a valid random nonce such that SHA3-256(Hr || nonce) starts with `pow_len` zeros.
 
    root = hashlib.sha3_256((transactions + PrevPoW).encode('utf-8')).hexdigest() #compute the merkle root
    root = root.encode('utf-8')

    target_prefix = '0' * PowLen  
    nonce = 0

    while True:
        nonce_b = nonce.to_bytes(32, byteorder='big')
        data = root + nonce_b
        
        hash_value = hashlib.sha3_256(data).hexdigest() #compute the SHA3-256 hash
        if hash_value.startswith(target_prefix):
            return nonce, hash_value

        nonce += 1