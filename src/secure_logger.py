import hashlib
import json
import time

class Block:
    """
    Represents a single block in the blockchain.
    Contains:
    - Index
    - Timestamp
    - Data (Security Event)
    - Previous Hash (Link to the chain)
    - Hash (Own unique ID)
    """
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        SHA-256 Hashing Algorithm.
        This ensures that if ANY data changes, the hash changes completely.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()

class BlockchainLogger:
    """
    Module 4: Blockchain-Secured Logger
    
    A tamper-proof ledger for security events.
    Once a block is added, it cannot be changed without breaking the chain.
    """
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        
    def create_genesis_block(self):
        """First block in the chain."""
        return Block(0, time.time(), "Genesis Block - System Initialized", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_log(self, event_type, person, details):
        """
        Creates a new block with security data and adds it to the chain.
        """
        prev_block = self.get_latest_block()
        
        data = {
            "event": event_type,
            "person": person,
            "details": details
        }
        
        new_block = Block(
            index=prev_block.index + 1,
            timestamp=time.time(),
            data=data,
            previous_hash=prev_block.hash
        )
        
        self.chain.append(new_block)
        print(f"[BLOCKCHAIN] Block #{new_block.index} added. Hash: {new_block.hash[:10]}...")

    def is_chain_valid(self):
        """
        Verifies the integrity of the blockchain.
        Returns True if safe, False if tampered.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i-1]

            # 1. Check if hash calculation is still correct (Data integrity)
            if current_block.hash != current_block.calculate_hash():
                print(f"[ALERT] Data tampering detected at Block {current_block.index}!")
                return False

            # 2. Check if previous hash matches (Chain integrity)
            if current_block.previous_hash != prev_block.hash:
                print(f"[ALERT] Chain broken at Block {current_block.index}!")
                return False
                
        return True

    def print_chain(self):
        print("\n--- IMMUTABLE SECURITY LEDGER ---")
        for block in self.chain:
            print(f"[{block.index}] \tTime: {time.ctime(block.timestamp)}")
            print(f"\tData: {block.data}")
            print(f"\tHash: {block.hash}")
            print(f"\tPrev: {block.previous_hash}")
            print("-" * 50)

# Independent Testing
if __name__ == "__main__":
    print("[TEST] Initializing Blockchain...")
    my_chain = BlockchainLogger()
    
    time.sleep(1)
    my_chain.add_log("ENTRY", "Vanapriya", "Authorized Access")
    
    time.sleep(1)
    my_chain.add_log("ALERT", "Unknown", "Intruder Detected")
    
    # Verify
    print(f"\nIs chain valid? {my_chain.is_chain_valid()}")
    
    my_chain.print_chain()
    
    # Simulation: Tampering Attack
    print("\n[ATTACK] Hacker trying to change logs...")
    my_chain.chain[1].data['event'] = "ENTRY" # Trying to change Intruder to Authorized
    
    print(f"Is chain valid after hack? {my_chain.is_chain_valid()}")
