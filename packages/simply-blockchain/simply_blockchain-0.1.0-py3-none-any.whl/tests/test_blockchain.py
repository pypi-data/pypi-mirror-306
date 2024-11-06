import unittest
from blockchain.blockchain import Blockchain

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        self.blockchain = Blockchain()

    def test_create_blockchain(self):
        self.assertEqual(len(self.blockchain.chain), 1)  # Should have the genesis block

    def test_add_transaction(self):
        self.blockchain.new_transaction("Alice", "Bob", 10)
        self.assertEqual(len(self.blockchain.current_transactions), 1)

    def test_mine_block(self):
        self.blockchain.new_transaction("Alice", "Bob", 10)
        nonce = self.blockchain.proof_of_work(self.blockchain.current_transactions)
        block = self.blockchain.new_block(self.blockchain.last_block.hash, nonce)
        self.assertEqual(len(self.blockchain.chain), 2)

    def test_valid_chain(self):
        self.assertTrue(self.blockchain.valid_chain())

if __name__ == '__main__':
    unittest.main()
