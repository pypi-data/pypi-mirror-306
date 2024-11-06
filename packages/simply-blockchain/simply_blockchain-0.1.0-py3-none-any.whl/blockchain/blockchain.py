import hashlib
import time
import json

# Block class that holds data
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.nonce = nonce

# Blockchain class to manage the chain
class Blockchain:
    def __init__(self):
        self.chain = []  # List to store the blockchain (list of blocks)
        self.current_transactions = []  # List to store transactions waiting to be added to a block
        self.create_genesis_block()  # Create the first block (genesis block)

    def create_genesis_block(self):
        # Genesis block (first block in the blockchain)
        # It has a fixed 'previous_hash' of "0" and no real data
        genesis_block = Block(
            index=0,  # First block, so index is 0
            previous_hash="0",  # First block has no previous block, hence "0"
            timestamp=int(time.time()),  # Current time as the timestamp
            data="Genesis Block",  # Data for the first block
            hash=self.hash_block(0, "0", int(time.time()), "Genesis Block", 0),  # Hash of the genesis block
            nonce=0  # No mining (proof-of-work) required for the genesis block
        )
        self.chain.append(genesis_block)  # Add the genesis block to the blockchain

    def new_block(self, previous_hash, nonce):
        # Create a new block and append it to the blockchain
        block = Block(
            index=len(self.chain),  # The index is the length of the chain (next block index)
            previous_hash=previous_hash,  # Previous block's hash
            timestamp=int(time.time()),  # Current time as timestamp
            data=self.current_transactions,  # The transactions in the current block
            hash=self.hash_block(len(self.chain), previous_hash, int(time.time()), self.current_transactions, nonce),  # Calculate the hash
            nonce=nonce  # Nonce found from proof-of-work algorithm
        )
        self.current_transactions = []  # Reset current transactions after adding them to the block
        self.chain.append(block)  # Add the new block to the chain
        return block  # Return the newly added block

    def new_transaction(self, sender, recipient, amount):
        # Add a new transaction to the list of current transactions
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        # Return the index of the block that will contain this transaction (next block)
        return self.last_block.index + 1

    @staticmethod
    def hash_block(index, previous_hash, timestamp, data, nonce):
        """
        Generate a hash for a block using the block's details (index, previous hash, timestamp, data, nonce)
        """
        block_string = json.dumps({
            'index': index,
            'previous_hash': previous_hash,
            'timestamp': timestamp,
            'data': data,
            'nonce': nonce
        }, sort_keys=True)  # Convert block data to a JSON string, ensuring the keys are sorted
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()  # Return the SHA-256 hash of the block string

    @property
    def last_block(self):
        # Returns the last block in the blockchain (the most recent one)
        return self.chain[-1]

    def proof_of_work(self, block_data):
        """
        Simple proof-of-work algorithm to find a valid nonce.
        The goal is to find a nonce such that the hash of the block starts with '0000'.
        This is done by brute-forcing different nonce values until the condition is met.
        """
        nonce = 0
        while True:
            # Generate a block hash for the current nonce
            block_hash = self.hash_block(len(self.chain), self.last_block.hash, int(time.time()), block_data, nonce)
            # Check if the hash starts with '0000' (difficulty)
            if block_hash.startswith("0000"):  # We are looking for a hash with four leading zeros
                return nonce  # Return the nonce when the condition is met
            nonce += 1  # Increment the nonce and try again

    def valid_chain(self):
        """
        Check if the blockchain is valid by verifying each block's hash and the chain's integrity.
        We check two conditions:
        1. Each block's previous hash matches the hash of the previous block.
        2. Each block's hash matches the expected hash based on its contents.
        """
        for i in range(1, len(self.chain)):  # Start checking from the second block (index 1)
            current = self.chain[i]  # Current block
            previous = self.chain[i - 1]  # Previous block

            # Check if the hash of the current block's previous hash matches the previous block's hash
            if current.previous_hash != previous.hash:
                return False  # If the hashes don't match, the chain is invalid

            # Check if the current block's hash is correct by recalculating it and comparing it with the stored hash
            if current.hash != self.hash_block(current.index, current.previous_hash, current.timestamp, current.data, current.nonce):
                return False  # If the hashes don't match, the chain is invalid

        return True  # The blockchain is valid if all blocks are properly linked and hashed
