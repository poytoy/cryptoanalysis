import random
import DS  # Importing DS.py for signing and verifying
import hashlib
import os

'''
transaction format:
*** Bitcoin transaction ***
Signature (s):
Signature (h):
Serial number:
Amount:
Payee public key (beta):
Payer public key (beta):
'''

def gen_random_tx(q, p, g):
    #generates a random blockchain transaction and signs it
    #returns the formatted transaction details including the signature as a string

    # generate 128 bit random serial number
    serial_number = random.getrandbits(128)

    # generate random amount [1, 1,000,000]
    amount = random.randint(1, 1000000)

    #generate payer and payee key pairs
    payer_alpha, payer_beta = DS.KeyGen(q, p, g)  # Payer's private and public keys
    payee_alpha, payee_beta = DS.KeyGen(q, p, g)  # Payee's private and public keys

    # combine transaction details as the message
    transaction_details = (
        f"Serial number: {serial_number}\n"
        f"Amount: {amount}\n"
        f"Payee public key (beta): {payee_beta}\n"
        f"Payer public key (beta): {payer_beta}\n"
    )
    message = transaction_details.encode('utf-8')

    # sign message using the payer's private key
    s, h = DS.SignGen(message, q, p, g, payer_alpha)

    # format transaction
    transaction = (
        "*** Bitcoin transaction ***\n"
        f"Signature (s): {s}\n"
        f"Signature (h): {h}\n"
        f"Serial number: {serial_number}\n"
        f"Amount: {amount}\n"
        f"Payee public key (beta): {payee_beta}\n"
        f"Payer public key (beta): {payer_beta}"
    )

    return transaction

def gen_random_txblock(q, p, g, TxCnt, filename):
    #generate “TxCnt” random transactions and write those transactions into the file “transactions.txt”
    
    if(TxCnt & (TxCnt - 1)): #make sure that “TxCnt” is always a power of two
        raise ValueError("TxCnt must be a power of two")

    mode = 'w' if os.path.exists(filename) else 'a' #if the file does not exist open a new one
    
    with open(filename, mode) as f:
        for i in range(TxCnt):
            tx = gen_random_tx(q, p, g)

            if i < TxCnt - 1:
                f.write(tx + "\n")
            else:
                f.write(tx) #don't add newline to the last transaction