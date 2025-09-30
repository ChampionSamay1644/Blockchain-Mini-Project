# Traffic Centre Blockchain System

## Table of Contents
- [Introduction](#introduction)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation and Setup](#installation-and-setup)
- [Usage Guide](#usage-guide)
- [Blockchain Implementation](#blockchain-implementation)
- [Use Cases and Real-world Applications](#use-cases-and-real-world-applications)
- [Future Enhancements](#future-enhancements)

## Introduction

The Traffic Centre Blockchain System is a decentralized application that leverages blockchain technology to maintain a secure and immutable record of vehicle information and registrations. The system provides a robust platform for vehicle identity management, demonstrating the fundamental concepts of blockchain technology including blocks, transactions, mining, and cryptographic hashing.

This project serves as both a learning tool for blockchain concepts and a foundation for real-world applications in vehicle registration systems, transportation management, and identity verification services.

## System Architecture

The system architecture consists of three main components:

```
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│                   │     │                   │     │                   │
│   Certificate     │     │                   │     │    Blockchain     │
│    Authority      │────▶│   Transaction     │────▶│      Mining       │
│                   │     │     Pool          │     │                   │
│                   │     │                   │     │                   │
└───────────────────┘     └───────────────────┘     └───────────────────┘
         │                                                   │
         │                                                   │
         │                                                   ▼
         │                                          ┌───────────────────┐
         │                                          │                   │
         └─────────────────────────────────────────▶│    Blockchain     │
                                                    │                   │
                                                    └───────────────────┘
```

1. **Certificate Authority**: Responsible for registering vehicle information and creating new transactions.
2. **Transaction Pool**: A temporary storage for unverified transactions.
3. **Blockchain Mining**: The process of validating transactions and adding them to blocks.
4. **Blockchain**: The immutable ledger that stores all verified transactions in blocks.

## Features

- **Vehicle Registration**: Register new vehicles with details such as registration number, license number, owner name, and pseudonym.
- **Blockchain Mining**: Mine blocks with verified vehicle transactions using Proof of Work (PoW) consensus.
- **Multiple Transactions per Block**: Support for batching multiple transactions in a single block for efficiency.
- **Blockchain Persistence**: The blockchain state is preserved between application runs.
- **Transaction Verification**: Verify the integrity of each transaction before adding it to a block.
- **Transaction Denial System**: Ability to deny suspicious transactions and store them separately for auditing purposes.
- **Block Explorer**: View all blocks in the blockchain with their hash values, nonce, and transactions.
- **Denied Transactions View**: Examine all previously denied transactions from a dedicated interface.
- **Modern UI**: An intuitive graphical user interface built with PyQt6.

## Technology Stack

- **Python**: Core programming language
- **PyQt6**: Modern GUI framework
- **pyscrypt**: Cryptographic hashing for blockchain security
- **Tkinter**: Alternative GUI framework (original implementation)

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. Clone the repository:
   ```
   git clone https://github.com/Blockchain-MiniProject.git
   cd Blockchain-MiniProject
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install required packages:
   ```
   pip install PyQt6 pyscrypt
   ```

4. Run the application:
   ```
   python Blockchain-Miniproject/main_pyqt6.py  # For PyQt6 version
   ```
   or
   ```
   python Blockchain-Miniproject/main.py  # For Tkinter version
   ```

## Usage Guide

### As Certificate Authority

1. Click on "Login As Certificate Authority" on the main screen.
2. Fill in the vehicle details:
   - Car Registration Number
   - License Number
   - Owner Name
   - Pseudonym (unique identifier for privacy)
3. Click "Submit" to add the vehicle information to the transaction pool.
4. You can submit multiple vehicle records.

### As Blockchain Miner

1. Click on "Login As Blockchain System Miner" on the main screen.
2. Review each transaction in the pool.
3. You have two options for each transaction:
   - Click "Verify and Add to Block" to add the transaction to the current block.
     - The system collects up to 5 transactions per block.
     - When a block is full, or you've reached the last transaction, mining will begin.
   - Click "Deny Transaction" to reject suspicious or fraudulent transactions.
     - Denied transactions are removed from the transaction pool.
     - They are stored separately in a denied transactions database for future reference.
4. The mining process uses a Proof of Work algorithm to find a valid nonce.
5. Once mining is successful, the block is added to the blockchain.
6. Navigate through transactions with "Next Transaction" and "Previous Transaction" buttons.

### View Blockchain

1. Click on "View Blocks in System" on the main screen.
2. This shows all blocks in the blockchain with:
   - Block number
   - Transactions contained in the block
   - Nonce value used to mine the block
   - Hash of the block

### View Denied Transactions

1. Click on "View Denied Transactions" on the main screen.
2. This displays all transactions that have been denied by miners:
   - Complete transaction details are preserved
   - Each denied transaction is displayed in a separate card
   - If no transactions have been denied, a message will indicate this

## Blockchain Implementation

### Core Components

#### Block Structure
Each block in the blockchain contains:
- Block number
- Multiple verified transactions
- Previous block hash (for chain integrity)
- Nonce (used in mining)
- Current block hash (created through mining)

#### Transaction Structure
Each transaction contains:
- Transaction number
- Car registration number
- License number
- Car owner name
- Pseudonym

#### Mining Process

The mining process implements a Proof of Work (PoW) consensus algorithm:

1. Transactions are verified and grouped into blocks.
2. The miner attempts to find a valid nonce that, when combined with the block data and previous block hash, produces a hash with a specific prefix (difficulty).
3. The SCRYPT hashing algorithm is used for mining.
4. The mining difficulty can be adjusted to control block creation time.

```python
# Mining algorithm pseudocode
def mine(transactions, last_hash):
    difficulty = 2  # Number of leading zeros required
    prefix_str = '0' * difficulty
    blocknumber = get_next_block_number()
    
    for nonce in range(MAX_NONCE):
        mine_string = transactions + last_hash + str(blocknumber)
        text = mine_string + str(nonce)
        new_hash = SCRYPT(text)
        
        if new_hash.startswith(prefix_str):
            # Valid block found
            save_block(blocknumber, transactions, nonce, new_hash)
            return new_hash
    
    # If no valid nonce found
    raise Exception("Mining failed: could not find valid nonce")
```

## Use Cases and Real-world Applications

### Traffic Management Systems

- **Vehicle Identity Management**: Secure and immutable vehicle registration records.
- **Traffic Violations Tracking**: Record traffic violations linked to specific vehicles.
- **Toll Collection Systems**: Automate and secure toll payments using pseudonyms.

### Supply Chain for Vehicles

- **Vehicle Parts Tracking**: Track genuine parts from manufacturer to end-user.
- **Vehicle History**: Maintain a complete history of the vehicle including repairs and accidents.
- **Ownership Transfers**: Record all ownership changes securely.

### Smart Cities Integration

- **Automated Parking Systems**: Secure identity verification for parking access.
- **Public Transport Integration**: Single identity system for multiple transport modes.
- **Congestion Management**: Dynamic pricing based on vehicle identity and traffic patterns.

### Insurance Applications

- **Risk Assessment**: Accurate vehicle history for risk assessment.
- **Claim Processing**: Streamlined and fraud-resistant claim processing.
- **Usage-based Insurance**: Secure tracking of vehicle usage patterns.

## Future Enhancements

1. **Distributed Network**: Implement a peer-to-peer network for true decentralization.
2. **Smart Contracts**: Add support for automated contract execution (e.g., transfer of ownership).
3. **Mobile Application**: Develop a companion mobile app for on-the-go access.
4. **Advanced Cryptography**: Implement zero-knowledge proofs for enhanced privacy.
5. **Integration APIs**: Create APIs for integration with other systems like traffic control, insurance, etc.
6. **Consensus Improvements**: Explore alternative consensus mechanisms like Proof of Stake.
7. **Data Analytics**: Implement analytics on the blockchain data for traffic pattern analysis.
