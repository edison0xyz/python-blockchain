# blockchain.py: simple implementation of blockchain

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

    # newTransaction - interface method
    def newTransaction(self, sender, recipient, message):

        if not self.validateTransaction(sender, message) and self.getLastBlock()['index'] != 1:
            return False
        d = {}
        d['sender'] = sender
        d['recipient'] = recipient
        d['message'] = message
        self.current_transactions.append(d)
        return True

    # mining function: mine the current transactions into a block
    # before putting it on the blockchain. Uses POW. 
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

    def getLastBlock(self):
        return self.chain[-1]

    # given a userid, returns the balance
    def getBalance(self, user_address): 
        amount = 0.0
        for blk in self.chain[1:]:
            transactions = blk['transactions']
            for txn in transactions:
                if txn['recipient'] == user_address:
                    amount += float(txn['message'])
                if txn['sender'] == user_address:
                    amount -= float(txn['message'])
        return amount

    # helper - to check for double-spending before coin is mined
    def getBalanceFromCurrentTransactions(self, user_address):
        amount = 0.0
        for txn in self.current_transactions:
            if txn['recipient'] == user_address:
                amount += float(txn['message'])
            if txn['sender'] == user_address:
                amount -= float(txn['message'])
        return amount

    # helper function for newTransaction. Given a sender address, validate if
    # user has sufficient balance
    # isMinder (boolean): if it is a miner, then we will check only against
    # confirmed blocks. If we are checking a transaction before putting it on
    # the chain, then we have to check against the current transactions

    def validateTransaction(self, sender, message):
        if not str(message).isdigit() or float(message) < self.token_currentsupply:
            return False
        amount = float(message)
        # if sender == 0, this transaction is a mine transaction
        # ignore validation if currentblock is the genesis block
        if sender != 0:
            confirmedBalance = self.getBalance(sender)
            balanceFromTransactionPool = self.getBalanceFromCurrentTransactions(sender)
            if confirmedBalance + balanceFromTransactionPool < amount:
                return False
        return True

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