# main.py: main class to call functions from blockchain.py

from Blockchain import Blockchain

bc = Blockchain()

def getFullChain():
    return bc.chain


# bootstrapping data - userid 1,2,3 has mined 500 tokens each
def load():
    data = [
        [0, 1, 500],
        [0, 2, 500],
        [0, 3, 500],
    ]
    for x in data:
        bc.newTransaction(x[0], x[1], x[2])
    bc.mine(1)

def test():
    # test case 1
    for i in range(1,4):
        amt = 600 if i == 1 else 500
        print(bc.getBalance(i))
        assert bc.getBalance(i) == amt
    print("Test Case 2 Passed")
    #bc.mine(5)
    #print(getFullChain())
load()
test()
