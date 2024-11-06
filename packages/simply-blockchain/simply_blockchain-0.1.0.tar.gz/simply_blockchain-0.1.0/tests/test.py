from blockchain.blockchain import Blockchain

# Create an instance of the Blockchain
blockchain = Blockchain()

# Add some transactions
blockchain.new_transaction("Alice", "Bob", 10)
blockchain.new_transaction("Bob", "Charlie", 5)

# Mine a block (finding a valid nonce and adding the block)
nonce = blockchain.proof_of_work(blockchain.current_transactions)
block = blockchain.new_block(blockchain.last_block.hash, nonce)

# Print all blocks in the blockchain
for block in blockchain.chain:
    print(f"Block #{block.index}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Data: {block.data}")
    print(f"Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}")
    print("-" * 60)

# Check if the blockchain is valid
print("Is the blockchain valid?", blockchain.valid_chain())
