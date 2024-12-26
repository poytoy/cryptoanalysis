import hashlib

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

def read_transactions(filename: str) -> list:
    transactions = []
    
    with open(filename, 'r') as file:
        current_transaction = ""
        
        for line in file:
            if line.strip() == "*** Bitcoin transaction ***":
                if current_transaction:
                    transactions.append(current_transaction.strip())
                current_transaction = ""
            else:
                current_transaction += line

        if current_transaction:
            transactions.append(current_transaction.strip()) #add the last one

    return transactions

def PoW(pow_len, q, p, g, txCnt, filename):
    #finds a valid random nonce such that SHA3-256(Hr || nonce) starts with `pow_len` zeros.
    transactions= read_transactions(filename)
    parsed_transactions=[tx for tx in transactions[:txCnt]]
 
    root = merkle_root(parsed_transactions)
    root = root.encode('utf-8')

    target_prefix = '0' * pow_len  
    nonce = 0

    while True:
        nonce_b = nonce.to_bytes(32, byteorder='big')
        data = root + nonce_b
        
        hash_value = hashlib.sha3_256(data).hexdigest() #compute the SHA3-256 hash
        if hash_value.startswith(target_prefix):
            return  hash_value

        nonce += 1
        
def CheckPow(p, q, g, PoWLen, TxCnt, filename):
    pow_hash=PoW(PoWLen, q, p, g, TxCnt, filename)

    if pow_hash.startswith('0' * PoWLen):
        return str(pow_hash) #return the valid nonce
    return str("")