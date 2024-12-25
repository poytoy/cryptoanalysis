import hashlib
import os
# Function to compute the SHA3-256 hash of a given string
def sha3_256(data):
    """Hash function for SHA3-256"""
    return hashlib.sha3_256(data.encode('utf-8')).hexdigest()
def merkle_root(transactions: list) -> str:
    # Step 1: Hash each transaction
    hashes = [sha3_256(tx) for tx in transactions]
    
    # Step 2: Combine hashes pair by pair until one hash remains (Merkle root)
    while len(hashes) > 1:
        new_hashes = []
        for i in range(0, len(hashes), 2):
            if i + 1 < len(hashes):
                combined = hashes[i] + hashes[i + 1]
            else:
                combined = hashes[i] + hashes[i]  # If odd number of hashes, duplicate the last one
            new_hashes.append(sha3_256(combined))
        hashes = new_hashes
    
    # Step 3: The remaining hash is the Merkle root
    return hashes[0]
def parse_transaction(transaction_str: str) -> str:
    """
    Extract relevant data from the transaction (signature, serial number, etc.)
    and return a string that will be hashed to form a Merkle leaf.
    """
    # Here, we will simply return the raw transaction string, 
    # but in practice you would extract specific fields to form a structured string.
    return transaction_str
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
            transactions.append(current_transaction.strip())  # Add the last one

    return transactions
def read_and_root(parsed_transactions):
    # Read transactions from the file
    # transactions = read_transactions("transactions.txt")
    # # Parse each transaction into a hashable string (this is just an example)
    # parsed_transactions = [parse_transaction(tx) for tx in transactions]
    
    # Compute the Merkle root
    root = merkle_root(parsed_transactions)

    return root


#lets enter  a Nonece to Merkle Tree root!
def PoW(pow_len,q,p,g,txCnt,filename):#(PoWLen, q, p, g, TxCnt, "transactions.txt"): root,pow_len
    """Finds a valid random nonce such that SHA3-256(Hr || nonce) starts with `pow_len` zeros."""
    transactions= read_transactions(filename)
    parsed_transactions=[parse_transaction(tx) for tx in transactions[:txCnt]]
 
    root = read_and_root(parsed_transactions)

    target_prefix = '0' * pow_len  
    root = root.encode('utf-8')
    while True:
        
        nonce = os.urandom(32)  
        nonce=nonce.hex()
        nonce = nonce.encode('utf-8')
       
        
        data =root + nonce
        
        # Compute the SHA3-256 hash
        hash_value = hashlib.sha3_256(data).hexdigest()
        if hash_value.startswith(target_prefix):
            return  hash_value
        
def CheckPow(p, q, g, PoWLen, TxCnt, filename):

    pow_hash=PoW(PoWLen, q, p, g, TxCnt, filename)
    if pow_hash.startswith('0' * PoWLen):
        return str(pow_hash)  # Return the valid nonce
    return str("")