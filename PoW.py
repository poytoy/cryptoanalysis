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