import random
import DS  # Importing DS.py for signing and verifying
import hashlib

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
        f"Payer public key (beta): {payer_beta}"
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
        f"Payer public key (beta): {payer_beta}\n"
    )

    return transaction

def main():
    q, p, g = DS.GenerateOrRead("pubparams.txt")

    transaction = gen_random_tx(q, p, g)
    print(f"Generated Transaction:{transaction}")

    print("Verifying Transaction Signature...")
    lines = transaction.split('\n')
    s = int(lines[1].split(": ")[1])  # Extract Signature s
    h = int(lines[2].split(": ")[1])  # Extract Signature h
    payer_pk = int(lines[6].split(": ")[1])  # Extract Payer's public key

    # Reconstruct the message (transaction details) for verification
    message = '\n'.join(lines[3:7]).encode('utf-8')

    # Verify the signature
    if DS.SignVer(message, s, h, q, p, g, payer_pk) == 0:
        print("Transaction signature is VALID.")
    else:
        print("Transaction signature is INVALID.")

    #test with these
    #CheckTransaction(q, p, g)
    #CheckBlockofTransactions()

if __name__ == "__main__":
    main()