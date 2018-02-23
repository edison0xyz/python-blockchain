# blockchain.py: simple implementation of blockchain. Does not
# support multi-user platform. POW is too simple too. 


from time import time
import hashlib
import json

DEBUG = False
def debug_print(message):
    print(message) if DEBUG else ""

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        self.token_currentsupply = 0
        self.token_maxSupply = 10000

        debug_print("Creating genesis block..")
        blk = self.create_block(prev=1, proof=1)
        debug_print(blk)
        self.chain.append(blk)
        debug_print("gen block created")

    @staticmethod
    def hash(block): 
        blk_str = json.dumps(block).encode()
        hashed_result = hashlib.sha256(blk_str).hexdigest()
        debug_print(hashed_result)
        return hashed_result
    
    def create_block(self, prev, proof):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'prev_hash': prev or self.hash(self.chain[-1]),
        }
        return block


    def getLastBlock(self):
        return self.chain[-1]

    def getBalance(self, userid): 
        amount = 0.0
        for blk in self.chain[1:]:
            transactions = blk['transactions']
            for txn in transactions:
                if txn['recipient'] == userid:
                    amount += float(txn['message'])
                if txn['sender'] == userid:
                    amount -= float(txn['message'])
        return amount


    def validateTransaction(self, sender, recipient, message):
        if not str(message).isdigit() or float(message) < self.token_currentsupply:
            return False
        amount = float(message)
        if sender != 0 and self.getBalance(sender) < amount:
            return False
        return True

    def newTransaction(self, sender, recipient, message):
        if not self.validateTransaction(sender, recipient, message):
            return 
        if not self.validateTransaction(sender, recipient, message):
            return
        d = {}
        d['sender'] = sender
        d['recipient'] = recipient
        d['message'] = message
        self.current_transactions.append(d)

    def mine(self, userid):
        debug_print("mining block")
        last_blk = self.getLastBlock()

        prev_proof = last_blk['proof']
        proof = self.proof_of_work(prev_proof)

        # once proof of work is verified, add rewards and mine the block

        self.newTransaction(0, userid, 100)
        newBlock = self.create_block(prev_proof, proof)
        self.chain.append(newBlock)
        self.current_transactions = [] 

        debug_print("Mined block: {}".format(newBlock['index']))

    # ===== consensus layer ==========



    # proof_of_work will keep running until a solution has been obtained
    def proof_of_work(self, last_proof):
        proof = 0
        debug_print("Prev proof: " + str(last_proof))
        while not self.checkValid(last_proof, proof):
            proof+=1
        debug_print("New Proof: " + str(proof))
        return proof #solution found
    
    # helper checker function, check preceding zeroes in solution
    def checkValid(self, last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"