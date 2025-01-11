## cryptoanalysis
We have to fix block.txt file.
pdfte AddBlock2Chain(PoWLen, TxCnt, PrevBlock, block_candidate) diyor ama test dosyasında AddBlock2Chain(PoWLen, TxCnt, block_candidate, PrevBlock) kullanılmış onun gibi yapıyorum fyi
# phase I
This part is about digital signatures and blockchain transactions.

What files does
DS.py: Create functions for signing, verifying, and managing keys.
Tx.py: Generate and verify blockchain transactions.
Use PhaseI_Test.py to make sure everything works:
'''bash
python PhaseI_Test.py
'''

# Phase II
This phase is about enhancing the cryptocurrency system by generating blocks of transactions and implementing Proof-of-Work (PoW).

PoW.py: Computes hash, then calculates merkle root of transactions implements proof of work algorithm by calculating nonce based on pow lenght specified.
Use PhaseII_Test.py to make sure everything works:
'''bash
python PhaseII_Test.py
'''

# Phase III
This phase focuses on two main tasks:

You can check ECDSA_Sample to explore the logic behind ECDSA procedures 
ECDSA.py: ECDSA Integration, Implementing elliptic curve digital signatures.
ChainGen.py: Blockchain Generation, Creating a blockchain by linking blocks using Proof-of-Work (PoW).

Use PhaseIII_Test.py to test your implementation:
Test I–III: Check ECDSA functions for key generation, signing, and transaction verification.
Test IV: Validate block linking and blockchain consistency.