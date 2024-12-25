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
    
    print(f"Merkle Root: {root}")
    return root


#lets enter  a Nonece to Merkle Tree root!
def PoW(root,pow_len):
    """Finds a valid random nonce such that SHA3-256(Hr || nonce) starts with `pow_len` zeros."""
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
    transactions= read_transactions(filename)
    parsed_transactions=[parse_transaction(tx) for tx in transactions[:TxCnt]]

    root = read_and_root(parsed_transactions)
    pow_hash=PoW(root,PoWLen)
    empty_str="1234"
    if pow_hash.startswith('0' * PoWLen):
        return str(pow_hash)  # Return the valid nonce
    return empty_str

def main():
    # Example Merkle root (replace with actual Merkle root)
    # Define the PoW length (number of leading zeros)
    pow_len = 5  # For example, PoWLen = 5
    n=CheckPow(26039433307800422174888769114527659404144539783096428019709032833391,29808528859494293238325907516066078728274934198623538302688976047031316822484482204373612821891882785291421056147796134283631143189676678942052429169559249158686990474016896322667367620601474302002628654745511332417025571367123256428856140260745363270347728495148005901869016947351519443614281272474593276911479090277994010655561264129637222171556063942532399193695821723250039717211699992417066965357436782881200835310458969476744836794800591311837613718768447643981004927700630092041730219332119302337442246165078173292710027500088640401059683914147699011697107726075824350680724853499141556196294503525772824164353,28167687707129733300182780916048278860830958274167498352564099770624938604490248174829410709316223682020229698757803420608807747054221582358805488697217106016571135260626579269478229621792386200036369156725763469217404178830352391490295027512701820828634822147356822076010191122977069905207868086760974153426322807320083767807476336224733065237034585407514213203537719176295022234598732189208571563720665895103437035569278706331696765692153806660558701545645354734528170064017327316573678458218048551461410241688949088151219372636936390889109891450497742663545673662343555799869575313337694597239118670724435351959473,3,64,"block_sample.txt")
    print(n)

    


# Run the main function
if __name__ == "__main__":
    main()
    
def CheckPow(p, q, g, PoWLen, TxCnt, filename):
    #returns an empty string if PoW of the block of transactions in “filename’ does not have preceding PoWLen hexadecimal 0s
    #otherwise, it returns the value of PoW

    pass

def PoW(PoWLen, q, p, g, TxCnt, filename):
    #reads the transactions in filename (i.e., “transactions.txt” generated in Test 1) and computes a PoW for the block
    #once your program finds the PoW for the block, it appends the nonce at the beginning of the block and writes it into a file with the name “block.txt”.
    #PoWLen must be at least 5 but test with 3 at first

    block = []

    with open("transactions.txt", 'r') as file:
        for _ in range(TxCnt):
            transaction = [file.readline().strip() for _ in range(7)]
            block.append(transaction) #add transaction to block vector
    
    #compute the root hash of the transactions using the Merkle tree, Hr, with SHA3 256
    #while the first PoWLen hexadecimal digits not 0: -> CheckPow(p, q, g, PoWLen, TxCnt, "block.txt")
        #generate random nonce
        #convert nonce to byte representation using to bytes()
        #append nonce to root hash
    #append the nonce at the beginning of the block and write it into “block.txt”.

