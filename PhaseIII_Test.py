#########################################
## Do not change this file             ##
## Your codes must work with this file ##
#########################################

import math
import random
import string
import warnings
import os.path
import sys
# These are the modules needed for elliptic curve cryptography
from ecpy.curves import Curve,Point
from Crypto.Hash import SHA3_256

# These are your modules
import ECDSA         # You have to submit this file,  
import ChainGen      # You have to submit this file  

TxLen = 9

# This is for generating a single transaction signed with ECDSA
def gen_random_tx(E):
    # ECDSA
    n = E.order
    P = E.generator
    # Payer
    payer_sk = random.randint(2,n-1)
    payer_pk = payer_sk*P
    # Payee
    payee_sk = random.randint(2,n-1)
    payee_pk = payee_sk*P
    # Transaction fields
    ser_no = random.randint(0, 2**128-1)
    amount = random.randint(1, 10000000)
    tx = "**** Bitcoin transaction ****\n"
    tx_ = "Serial number: " + str(ser_no) + "\n"
    tx_ += "Amount: " + str(amount) + "\n"
    tx_ += "Payee public key - x: " + str(payee_pk.x) + "\n"
    tx_ += "Payee public key - y: " + str(payee_pk.y) + "\n"
    tx_ += "Payer public key - x: " + str(payer_pk.x) + "\n"
    tx_ += "Payer public key - y: " + str(payer_pk.y) + "\n"
    # Sign
    (s, h) = ECDSA.SignGen(tx_.encode('UTF-8'), E, payer_sk)
    tx += "Signature (s): " + str(s) + "\n"
    tx += "Signature (h): " + str(h) + "\n"
    tx += tx_
    # Return the transaction
    return tx

# This is for generating TxCnt transactions, each of which is signed with ECDSA
def gen_random_txblock(E, TxCnt):
    tx_blk = ""
    for i in range(0, TxCnt):
        tx_blk += gen_random_tx(E)
    return tx_blk 


def CheckTransactions(filename, E):
    if os.path.isfile(filename):
        f = open(filename, "r")
        block = f.readlines()
        if len(block)%TxLen != 0:
            print("Incorrect file format")
            f.close()
            return -10000
        block_count = len(block)//TxLen
        for i in range(0, block_count):
            # coordinates of the public key point
            x1 = int(block[i*TxLen+7][22:-1])
            y1 = int(block[i*TxLen+8][22:-1])
            s = int(block[i*TxLen+1][15:-1])
            h = int(block[i*TxLen+2][15:-1])
            tx = "".join(block[i*TxLen+3: i*TxLen+9])
            # For the signature verfication
            payer_pk = Point(x1, y1, E)
            if ECDSA.SignVer(tx.encode('UTF-8'), s, h, E, payer_pk) != 0:
                return -1
        return 0
    else:
        print("File does not exist")
        return -10000

def CheckBlock(TxCnt, Block):
    hashTree = []
    # The PrevPow is at the top of the block, so read it first
    PrevPoW_ = Block.pop(0)
    PrevPoW_ = str(PrevPoW_.split(": ")[1].strip())  # Extract PoW
    PrevPoW = PrevPoW_.encode('utf-8')

    # The nonce is now at the top of the block, so read it next
    nonce_line = Block.pop(0)
    nonce = int(nonce_line.split(": ")[1].strip())  # Extract nonce value

    for i in range(0,TxCnt):
        transaction = "".join(Block[i*TxLen:(i+1)*TxLen])
        hashTree.append(SHA3_256.new(transaction.encode('UTF-8')).digest())
    t = TxCnt
    j = 0
    while(t>1):
        for i in range(j,j+t,2):
            hashTree.append(SHA3_256.new(hashTree[i]+hashTree[i+1]).digest())
        j += t
        t = t>>1

    H_r = hashTree[2*TxCnt-2]
    
    
    digest = H_r + PrevPoW + nonce.to_bytes((nonce.bit_length()+7)//8, byteorder = 'big')
    PoW = SHA3_256.new(digest).hexdigest()
    #print("H_R: ",H_r)
    return PoW, PrevPoW_

##############        
# Student Part
E = Curve.get_curve('secp256k1') # We will always use this curve

# Test I
#########
# Testing our version of ECDSA;
# Generate a signature and verify it
sA, QA = ECDSA.KeyGen(E)   # generate a secret/public key pair

message = b"When you can't find the sunshine, be the sunshine"
s, h = ECDSA.SignGen(message, E, sA)
if ECDSA.SignVer(message, s, h, E, QA)== 0: print("Test I: The signature verifies")
else: print("Test I: The signature DOES NOT verify")

# Test II
#########
# Testing our version of ECDSA against instructor's implementation
# Verify given and signature and a public key
message = b"The grass is greener where you water it"
QA = Point(0xb935f668ab9bfde44cf0064d3426dcc6de99c9a0f410cbeb360368f01e40c115, 
           0xedc0f29c9056dab53d36db41fcc4b0ee6a7b1e3bda71573cff860ed3bd7e6443,
        E)
s = 71377830883974214922838567734934785765591886671381396210676147950201761119704
h = 60333731355937835604264748455175544140321967376473797857716946010025483330243
if ECDSA.SignVer(message, s, h, E, QA)== 0: print("Test II: The signature verifies")
else: print("Test II: The signature DOES NOT verify")

# Test III
#########
# Generating random transactions signed by ECDSA
TxCnt = 32 # the number of transactions in the block
tx_blk = gen_random_txblock(E, TxCnt)   
fp = open("transactions.txt", "w")
fp.write(tx_blk)
fp.close()

# Verify the signatures of all your transactions in a block
ReturnCode = CheckTransactions("transactions.txt", E)
if ReturnCode == -10000: print("Test III: File Problem")
elif(ReturnCode < 0): print("Test III: Signature Problem in Transaction number", -ReturnCode)
elif ReturnCode == 0: print("Test III: All transactions verify")
else: print("Test III: Unexpected branching")

# Test IV
#########
# Generate the blockchain
TxCnt = 16       # number of transactions in a single block
ChainLen = 10    # number of blocks
PoWLen = 4
filename = "Block"
ctr = 0

# The first link in the chain 
# The block_candidate contains only the transactions; neither PrevPow nor nonce
PrevBlock = ""  # Previous block doesn't exist as this is the first link
transactions = gen_random_txblock(E, TxCnt) # generate random transactions
f = open("tmp.txt", "w")
f.write(transactions)
f.close()                                   # write the transactions into "tmp.txt"

f = open("tmp.txt", "r")
block_candidate = f.readlines()
f.close()                                   # read the transactions from "tmp.txt"

# Calculate the first block in the chain
NewBlock, PrevPoW = ChainGen.AddBlock2Chain(PoWLen, TxCnt, block_candidate, PrevBlock)
f = open(filename + "0.txt", "w")
f.write(NewBlock)
f.close()

# Create the other links in the chain
for i in range(1, ChainLen):
    # read the previous block from the file
    f = open(filename + str(i-1) + ".txt", "r")
    PrevBlock = f.readlines()  
    f.close()

    transactions = gen_random_txblock(E, TxCnt)
    f = open("tmp.txt", "w")
    f.write(transactions)
    f.close()

    f = open("tmp.txt", "r")
    block_candidate = f.readlines()
    f.close()    

    NewBlock, PrevPoW = ChainGen.AddBlock2Chain(PoWLen, TxCnt, block_candidate, PrevBlock)
    # Write the new block to a file 
    f = open(filename + str(i) + ".txt", "w")
    f.write(NewBlock)
    f.close()
    if PrevPoW[:PoWLen] != "0"*PoWLen:
        print("Block " + str(i) + " failed Test IV: BadPrevPoW")

# And check the blockchain
# First block
f = open(filename + "0.txt", "r")
Block = f.readlines()
f.close()
PoW, PrevPoW = CheckBlock(TxCnt, Block)
if PoW[0:PoWLen] == "0"*PoWLen: print("Block 0 passed Test IV")
else: print("Block 0 failed Test IV")

# And the subsequent blocks
for i in range(1, ChainLen):
    PrevPoW = PoW
    f = open(filename + str(i) + ".txt", "r")
    Block = f.readlines()
    f.close()
    PoW, PrevPoW_ = CheckBlock(TxCnt, Block)
    if PoW[0:PoWLen] == "0"*PoWLen and PrevPoW == PrevPoW_:
        print("Block " + str(i) + " passed Test IV")
    else: print("Block " + str(i) + " failed Test IV")
