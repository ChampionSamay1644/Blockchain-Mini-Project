import hashlib
import os
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, 
                           QHBoxLayout, QWidget, QTextEdit, QLineEdit, QGridLayout,
                           QFrame, QScrollArea, QSizePolicy, QMessageBox)
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt

# Import the original classes (with PyQt6 adaptations)
from client import *
from miner import *

class BlockchainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Traffic Centre Blockchain System")
        self.setMinimumSize(800, 600)
        self.center_on_screen()
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #000000;
            }
            QTextEdit {
                border: 2px solid #3498db;
                border-radius: 4px;
                background-color: #f8f9fa;
                color: #000000;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #3498db;
                border-radius: 4px;
                background-color: white;
                color: #000000;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        
        self.init_login_ui()
        self.transactions = []
        self.last_block_hash = ""
        self.last_transaction_index = 0

        # Create the Block class as in original code
        self.block = Block()
        
        # Load or initialize blockchain
        self.load_blockchain_data()

    def init_login_ui(self):
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header label with title
        header_label = QLabel("Traffic Centre Blockchain System")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #000000;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Create a container for buttons with some spacing
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)
        buttons_layout.setSpacing(15)
        
        # Create stylish buttons
        button_width = 300
        button_height = 50
        
        # CA Button
        ca_button = QPushButton("Login As Certificate Authority")
        ca_button.setFixedSize(button_width, button_height)
        ca_button.clicked.connect(self.open_certificate_authority)
        buttons_layout.addWidget(ca_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Miner Button
        miner_button = QPushButton("Login As Blockchain System Miner")
        miner_button.setFixedSize(button_width, button_height)
        miner_button.clicked.connect(self.open_blockchain_miner)
        buttons_layout.addWidget(miner_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # View Blocks Button
        blocks_button = QPushButton("View Blocks in System")
        blocks_button.setFixedSize(button_width, button_height)
        blocks_button.clicked.connect(self.view_blocks)
        buttons_layout.addWidget(blocks_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # View Denied Transactions Button
        denied_button = QPushButton("View Denied Transactions")
        denied_button.setFixedSize(button_width, button_height)
        denied_button.clicked.connect(self.view_denied_transactions)
        denied_button.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;
                color: white;
            }
            QPushButton:hover {
                background-color: #E64A19;
            }
        """)
        buttons_layout.addWidget(denied_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Exit Button
        exit_button = QPushButton("Exit")
        exit_button.setFixedSize(button_width, button_height)
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        exit_button.clicked.connect(self.close_application)
        buttons_layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add buttons container to main layout
        main_layout.addWidget(buttons_widget)
        
        # Add footer
        footer_label = QLabel("© 2025 Blockchain Traffic Management System")
        footer_label.setStyleSheet("color: #333333; font-size: 12px;")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(footer_label)

    def open_certificate_authority(self):
        self.hide()
        self.ca_window = CertificateAuthorityWindow(self)
        self.ca_window.show()
    
    def open_blockchain_miner(self):
        self.hide()
        self.miner_window = MinerWindow(self, self.last_block_hash)
        self.miner_window.show()
    
    def view_blocks(self):
        self.hide()
        self.blocks_window = BlocksWindow(self)
        self.blocks_window.show()
    
    def view_denied_transactions(self):
        self.hide()
        self.denied_transactions_window = DeniedTransactionsWindow(self)
        self.denied_transactions_window.show()
    
    def center_on_screen(self):
        # Center window on screen
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    
    def load_blockchain_data(self):
        # Check if blockchain files exist
        if os.path.exists("blocks.txt"):
            # Load last hash from blocks.txt
            with open("blocks.txt", "r") as f:
                blocks = f.readlines()
                if blocks:
                    last_block = blocks[-1].strip()
                    # Extract hash from the last line
                    hash_part = last_block.split("Hash: ")[-1].strip()
                    self.last_block_hash = hash_part
                    print(f"Loaded last block hash: {self.last_block_hash}")
                else:
                    # Empty file, initialize with Genesis block
                    self._initialize_genesis_block()
        else:
            # No blockchain file, initialize with Genesis block
            self._initialize_genesis_block()
    
    def _initialize_genesis_block(self):
        # Initialize blockchain with Genesis block
        t0 = 'Genesis Block'
        digest = hash(t0)
        self.last_block_hash = digest
        
        # Save Genesis block to file
        with open("blocks.txt", "w") as f:
            f.write(f"Block number: 0, Transaction: {{Genesis Block}}, Nonce: 0, Number of Transactions: 1, Hash: {digest}\n")
        
    def close_application(self):
        # Preserve blockchain data - don't delete files
        QApplication.quit()


class CertificateAuthorityWindow(QMainWindow):
    counter = 0
    
    @classmethod
    def load_transaction_counter(cls):
        # Initialize counter based on existing transactions
        cls.counter = 0
        if os.path.exists("vehicle_information.txt"):
            try:
                with open("vehicle_information.txt", "r") as f:
                    transactions = f.readlines()
                    for trans in transactions:
                        if trans.strip():
                            try:
                                # Extract transaction number
                                trans_num_str = trans.split("Transaction No: ")[1].split(",")[0]
                                trans_num = int(trans_num_str)
                                # Update counter to highest value
                                cls.counter = max(cls.counter, trans_num)
                            except (IndexError, ValueError):
                                # Skip malformed lines
                                pass
            except Exception as e:
                print(f"Error loading transaction counter: {e}")
    
    def center_on_screen(self):
        # Center window on screen
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("VANET Blockchain Login System")
        self.setMinimumSize(600, 500)
        self.center_on_screen()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_label = QLabel("Vehicle Registration Form")
        header_label.setStyleSheet("font-size: 22px; font-weight: bold; margin: 20px 0; color: #00FF00;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Form layout
        form_widget = QWidget()
        form_layout = QGridLayout(form_widget)
        form_layout.setSpacing(15)
        
        # Car Registration
        car_reg_label = QLabel("Car Registration Number:")
        self.car_reg_input = QLineEdit()
        self.car_reg_input.setPlaceholderText("e.g., KA01AB1234")
        form_layout.addWidget(car_reg_label, 0, 0)
        form_layout.addWidget(self.car_reg_input, 0, 1)
        
        # License Number
        license_label = QLabel("License Number:")
        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText("e.g., DL-0123456789")
        form_layout.addWidget(license_label, 1, 0)
        form_layout.addWidget(self.license_input, 1, 1)
        
        # Owner Name
        owner_label = QLabel("Owner Name:")
        self.owner_input = QLineEdit()
        self.owner_input.setPlaceholderText("e.g., John Doe")
        form_layout.addWidget(owner_label, 2, 0)
        form_layout.addWidget(self.owner_input, 2, 1)
        
        # Pseudonym
        pseudonym_label = QLabel("Pseudonym:")
        self.pseudonym_input = QLineEdit()
        self.pseudonym_input.setPlaceholderText("e.g., JD123")
        form_layout.addWidget(pseudonym_label, 3, 0)
        form_layout.addWidget(self.pseudonym_input, 3, 1)
        
        # Vehicle Type
        vehicle_type_label = QLabel("Vehicle Type:")
        self.vehicle_type_input = QLineEdit()
        self.vehicle_type_input.setPlaceholderText("e.g., Sedan, SUV, Truck")
        form_layout.addWidget(vehicle_type_label, 4, 0)
        form_layout.addWidget(self.vehicle_type_input, 4, 1)
        
        # Manufacture Year
        year_label = QLabel("Manufacture Year:")
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("e.g., 2022")
        form_layout.addWidget(year_label, 5, 0)
        form_layout.addWidget(self.year_input, 5, 1)
        
        # Add form to main layout
        main_layout.addWidget(form_widget)
        
        # Buttons
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(20, 20, 20, 20)
        buttons_layout.setSpacing(20)
        
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.save_info)
        submit_button.setMinimumHeight(40)
        
        clear_button = QPushButton("Clear Form")
        clear_button.clicked.connect(self.clear_form)
        clear_button.setMinimumHeight(40)
        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        
        exit_button = QPushButton("Exit")
        exit_button.setMinimumHeight(40)
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        exit_button.clicked.connect(self.exit_to_main)
        
        buttons_layout.addWidget(submit_button)
        buttons_layout.addWidget(clear_button)
        buttons_layout.addWidget(exit_button)
        
        main_layout.addWidget(buttons_widget)

    def clear_form(self):
        """Clear all input fields in the form"""
        self.car_reg_input.clear()
        self.license_input.clear()
        self.owner_input.clear()
        self.pseudonym_input.clear()
        
        # Clear additional fields if they exist
        if hasattr(self, 'vehicle_type_input'):
            self.vehicle_type_input.clear()
        if hasattr(self, 'year_input'):
            self.year_input.clear()
            
        # Set focus back to the first field
        self.car_reg_input.setFocus()

    def check_duplicate_car_registration(self, car_reg_info):
        """Check if a car registration number already exists in the transaction file"""
        if not os.path.exists("vehicle_information.txt"):
            return False
            
        try:
            with open("vehicle_information.txt", "r") as file:
                for line in file:
                    if f"Car Registration Number: {car_reg_info}" in line:
                        return True
            return False
        except Exception:
            # If there's an error reading the file, proceed assuming it's not a duplicate
            return False
    
    def save_info(self):
        car_reg_info = self.car_reg_input.text().strip()
        license_info = self.license_input.text().strip()
        owner_info = self.owner_input.text().strip()
        pseudonym_info = self.pseudonym_input.text().strip()
        vehicle_type_info = self.vehicle_type_input.text().strip() if hasattr(self, 'vehicle_type_input') else ""
        year_info = self.year_input.text().strip() if hasattr(self, 'year_input') else ""
        
        # Validate required fields
        if not car_reg_info or not license_info or not owner_info or not pseudonym_info:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Missing Information")
            msg_box.setText("Please fill in all required fields.")
            msg_box.setDetailedText("Car Registration Number, License Number, Owner Name, and Pseudonym are required fields.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            return
            
        # Check for duplicate car registration
        if self.check_duplicate_car_registration(car_reg_info):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Duplicate Registration")
            msg_box.setText(f"Car with registration number '{car_reg_info}' already exists in the system.")
            msg_box.setInformativeText("Please use a different registration number or check existing records.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            return
        
        CertificateAuthorityWindow.counter += 1
        
        # Save to file
        try:
            file = open("vehicle_information.txt", "a+")
            file.write("Transaction No: " + str(CertificateAuthorityWindow.counter) + ", ")
            file.write("Car Registration Number: " + car_reg_info + ", ")
            file.write("License Number: " + license_info + ", ")
            file.write("Car Owner Name: " + owner_info + ", ")
            file.write("Pseudonym: " + pseudonym_info)
            
            # Add new fields if they exist
            if vehicle_type_info:
                file.write(", Vehicle Type: " + vehicle_type_info)
            if year_info:
                file.write(", Manufacture Year: " + year_info)
                
            file.write("\n")
            file.close()
        except Exception as e:
            CertificateAuthorityWindow.counter -= 1  # Revert counter increase
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle("Error")
            msg_box.setText("Could not save transaction.")
            msg_box.setDetailedText(f"Error: {str(e)}")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            return
        
        # Show success message
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setWindowTitle("Success")
        msg_box.setText("Vehicle information submitted successfully!")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
        
        # Clear inputs
        self.clear_form()
        if hasattr(self, 'year_input'):
            self.year_input.setText('')
        
        # Show options dialog
        self.hide()
        self.options_window = OptionsWindow(self)
        self.options_window.show()

    def exit_to_main(self):
        self.hide()
        if self.parent:
            self.parent.show()


class OptionsWindow(QMainWindow):
    def center_on_screen(self):
        # Center window on screen
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.main_parent = parent.parent if parent else None
        
        self.setWindowTitle("Please Choose")
        self.setMinimumSize(500, 200)
        self.center_on_screen()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Thank you message
        thank_label = QLabel("Thank you for submitting!")
        thank_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px 0; color: #006600;")
        thank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(thank_label)
        
        # Buttons
        submit_another = QPushButton("Submit another car information record")
        submit_another.clicked.connect(self.submit_another_action)
        main_layout.addWidget(submit_another)
        
        go_back = QPushButton("Go back to login page")
        go_back.clicked.connect(self.go_back_action)
        main_layout.addWidget(go_back)

    def submit_another_action(self):
        self.hide()
        if self.parent:
            self.parent.show()

    def go_back_action(self):
        self.hide()
        if self.parent:
            self.parent.hide()
        if self.main_parent:
            self.main_parent.show()


class MinerWindow(QMainWindow):
    blocknumber = 0
    
    def center_on_screen(self):
        # Center window on screen
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
    def load_block_number(self):
        # Initialize block number based on existing blocks
        MinerWindow.blocknumber = 0
        if os.path.exists("blocks.txt"):
            with open("blocks.txt", "r") as f:
                blocks = f.readlines()
                if blocks:
                    for block in blocks:
                        if block.strip():  # Skip empty lines
                            try:
                                # Extract block number from line
                                block_num_str = block.split("Block number: ")[1].split(",")[0]
                                block_num = int(block_num_str)
                                # Update the block number to the highest value found
                                MinerWindow.blocknumber = max(MinerWindow.blocknumber, block_num)
                            except (IndexError, ValueError):
                                # Skip malformed lines
                                pass
                    # We'll start with the next block number
                    print(f"Loaded block number: {MinerWindow.blocknumber}")
    
    def __init__(self, parent=None, last_hash=""):
        super().__init__()
        self.parent = parent
        self.last_hash = last_hash
        self.count = 0
        self.new_hash = ""
        self.transactions = []
        
        self.setWindowTitle("Blockchain Miner")
        self.setMinimumSize(700, 500)
        self.center_on_screen()
        
        # Load block number from blockchain file to ensure continuity
        self.load_block_number()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Check for existing transactions
        if os.path.exists("vehicle_information.txt"):
            try:
                f = open("vehicle_information.txt", "r")
                content = f.read()
                f.close()
                if content.strip():  # Make sure file is not empty
                    self.transactions = content.split('\n')
                    # Remove empty entries
                    self.transactions = [t for t in self.transactions if t.strip()]
            except Exception as e:
                print(f"Error loading transactions: {e}")
                self.transactions = []
            
            # Header
            header_label = QLabel("Verify Transaction")
            header_label.setStyleSheet("font-size: 22px; font-weight: bold; margin: 20px 0; color: #00FF00;")
            header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(header_label)
            
            # Transaction display
            self.transaction_display = QTextEdit()
            self.transaction_display.setReadOnly(True)
            self.transaction_display.setMinimumHeight(150)
            self.transaction_display.setStyleSheet("""
                background-color: #f8f9fa;
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 10px;
                font-family: monospace;
                font-size: 14px;
                color: #000000;
                font-weight: bold;
            """)
            
            # Display first transaction
            if self.transactions:
                transaction = str(self.transactions[self.count]).replace(',', '\n')
                # Format transaction data for better readability
                formatted_transaction = self._format_transaction_data(transaction)
                self.transaction_display.setText(formatted_transaction)
                
            main_layout.addWidget(self.transaction_display)
            
            # Buttons
            buttons_widget = QWidget()
            buttons_layout = QHBoxLayout(buttons_widget)
            
            verify_button = QPushButton("Verify and Add to Block")
            verify_button.clicked.connect(self.add_to_block)
            verify_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            buttons_layout.addWidget(verify_button)
            
            # Add deny transaction button
            deny_button = QPushButton("Deny Transaction")
            deny_button.clicked.connect(self.deny_transaction)
            deny_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
            """)
            buttons_layout.addWidget(deny_button)
            
            # Add previous button
            self.prev_button = QPushButton("Previous Transaction")
            self.prev_button.clicked.connect(self.prev_transaction)
            if self.count == 0:  # Disable if first transaction
                self.prev_button.setEnabled(False)
            buttons_layout.addWidget(self.prev_button)
            
            # Next button
            next_button = QPushButton("Next Transaction")
            next_button.clicked.connect(self.next_transaction)
            buttons_layout.addWidget(next_button)
            
            exit_button = QPushButton("Exit")
            exit_button.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            exit_button.clicked.connect(self.exit_to_main)
            buttons_layout.addWidget(exit_button)
            
            main_layout.addWidget(buttons_widget)
            
        else:
            # No transactions
            no_trans_label = QLabel("No transaction present in transaction repository")
            no_trans_label.setStyleSheet("font-size: 18px; color: #00FF00; margin: 50px 0;")
            no_trans_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(no_trans_label)
            
            exit_button = QPushButton("Exit")
            exit_button.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            exit_button.clicked.connect(self.exit_to_main)
            main_layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def check_duplicate_in_current_block(self, transaction):
        """Check if a transaction is already added to the current block"""
        if not hasattr(self, 'current_block_transactions'):
            return False
            
        # Extract car registration number from transaction
        car_reg_match = None
        for part in transaction.split(','):
            if "Car Registration Number:" in part:
                car_reg_match = part.strip()
                break
                
        if not car_reg_match:
            return False
            
        # Check if this car registration exists in any transaction in current block
        for existing_trans in self.current_block_transactions:
            if car_reg_match in existing_trans:
                return True
                
        return False
            
    def check_duplicate_in_blockchain(self, transaction):
        """Check if a transaction is already in the blockchain"""
        if not os.path.exists("blocks.txt"):
            return False
            
        # Extract car registration number from transaction
        car_reg_match = None
        for part in transaction.split(','):
            if "Car Registration Number:" in part:
                car_reg_match = part.strip()
                break
                
        if not car_reg_match:
            return False
            
        # Check blocks.txt for this car registration
        try:
            with open("blocks.txt", "r") as f:
                blockchain_content = f.read()
                if car_reg_match in blockchain_content:
                    return True
        except Exception:
            pass
            
        return False
    
    def add_to_block(self):
        # Get the transactions to add to the block
        current_transaction = self.transactions[self.count]
        
        # Check if we already have a block being built and how many transactions it has
        block_transactions = []
        max_transactions_per_block = 5  # Maximum transactions per block
        
        if hasattr(self, 'current_block_transactions'):
            block_transactions = self.current_block_transactions
        else:
            self.current_block_transactions = block_transactions
        
        # Check if transaction is already in the current block or blockchain
        if self.check_duplicate_in_current_block(current_transaction):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Duplicate Transaction")
            msg_box.setText("This vehicle is already in the current block.")
            msg_box.setInformativeText("Cannot add the same vehicle transaction twice.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            # Move to next transaction
            self.next_transaction()
            return
            
        if self.check_duplicate_in_blockchain(current_transaction):
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Already in Blockchain")
            msg_box.setText("This vehicle is already recorded in the blockchain.")
            msg_box.setInformativeText("Cannot add a vehicle that already exists in the blockchain.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            # Move to next transaction
            self.next_transaction()
            return
            
        # Add current transaction to the block
        block_transactions.append(current_transaction)
        
        # If we have reached the maximum transactions per block or this is the last transaction
        if len(block_transactions) >= max_transactions_per_block or self.count == len(self.transactions) - 1:
            self.hide()
            # Join all transactions with a special delimiter
            block_content = "\n---TRANSACTION---\n".join(block_transactions)
            self.mine_window = MiningWindow(self, block_content, self.last_hash, block_transactions)
            self.mine_window.show()
            # Clear the current block after mining
            self.current_block_transactions = []
        else:
            # If block isn't full yet, just move to next transaction
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Transaction Added")
            msg_box.setText(f"Transaction added to block. {len(block_transactions)} of {max_transactions_per_block} transactions in current block.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            # Move to next transaction
            self.next_transaction()

    def prev_transaction(self):
        if not self.transactions or self.count <= 0:
            return
            
        self.count -= 1
        transaction = str(self.transactions[self.count]).replace(',', '\n')
        # Format transaction data for better readability
        formatted_transaction = self._format_transaction_data(transaction)
        self.transaction_display.setText(formatted_transaction)
        
        # Enable/disable buttons based on position
        self.prev_button.setEnabled(self.count > 0)
            
    def deny_transaction(self):
        """Deny the current transaction and save it to denied_transactions.txt"""
        if not self.transactions or self.count >= len(self.transactions):
            return
            
        # Get current transaction
        current_transaction = self.transactions[self.count]
        
        # Add to denied transactions file
        try:
            # Create the denied_transactions.txt file if it doesn't exist
            with open("denied_transactions.txt", "a+") as file:
                file.write(current_transaction + "\n")
                
            # Show confirmation message
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("Transaction Denied")
            msg_box.setText("Transaction has been denied and saved to denied_transactions.txt")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            
            # Remove transaction from list immediately
            self.transactions.pop(self.count)
            
            # Update transaction file with remaining transactions
            with open("vehicle_information.txt", "w") as file:
                if self.transactions:
                    file.write("\n".join(self.transactions) + "\n")
            
            # Handle navigation after removal
            if not self.transactions:
                # No transactions left
                self.hide()
                self.end_window = TransactionEndWindow(self)
                self.end_window.show()
            else:
                # Adjust count if we removed the last transaction
                if self.count >= len(self.transactions):
                    self.count = len(self.transactions) - 1
                
                # Update display with current transaction
                transaction = str(self.transactions[self.count]).replace(',', '\n')
                formatted_transaction = self._format_transaction_data(transaction)
                self.transaction_display.setText(formatted_transaction)
                self.prev_button.setEnabled(self.count > 0)
        except Exception as e:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle("Error")
            msg_box.setText(f"Failed to deny transaction: {str(e)}")
            msg_box.setDetailedText(str(e))
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
    
    def next_transaction(self):
        if not self.transactions:
            return
            
        self.count += 1
        if self.count >= len(self.transactions):
            self.hide()
            self.end_window = TransactionEndWindow(self)
            self.end_window.show()
        else:
            transaction = str(self.transactions[self.count]).replace(',', '\n')
            # Format transaction data for better readability
            formatted_transaction = self._format_transaction_data(transaction)
            self.transaction_display.setText(formatted_transaction)
            # Enable previous button as we're not on the first transaction
            self.prev_button.setEnabled(True)

    def exit_to_main(self):
        self.hide()
        if self.parent:
            self.parent.show()

    def _format_transaction_data(self, transaction_text):
        """Format transaction data for better display"""
        # Split by lines
        lines = transaction_text.split('\n')
        formatted_lines = []
        
        for line in lines:
            if ':' in line:
                # Split at the first colon
                parts = line.split(':', 1)
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ""
                # Make key bold and colored
                formatted_line = f"{key}: {value}"
                formatted_lines.append(formatted_line)
            else:
                formatted_lines.append(line)
                
        return '\n'.join(formatted_lines)


class MiningWindow(QMainWindow):
    def center_on_screen(self):
        # Center window on screen
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    def __init__(self, parent=None, transaction="", last_hash="", original_transactions=None):
        super().__init__()
        self.parent = parent
        self.transaction = transaction  # This can now contain multiple transactions
        self.last_hash = last_hash
        self.original_transactions = original_transactions or []  # List of original transactions
        
        self.setWindowTitle("Mining Block...")
        self.setMinimumSize(700, 500)
        self.center_on_screen()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_label = QLabel("Transaction added to block")
        header_label.setStyleSheet("font-size: 22px; font-weight: bold; margin: 20px 0; color: #2C3E50;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Transaction display
        self.transaction_display = QTextEdit()
        self.transaction_display.setReadOnly(True)
        self.transaction_display.setMinimumHeight(150)
        self.transaction_display.setStyleSheet("""
            background-color: #f8f9fa;
            border: 2px solid #3498db;
            border-radius: 8px;
            padding: 10px;
            font-family: monospace;
            font-size: 14px;
            color: #000000;
            font-weight: bold;
        """)
        
        # Display transaction
        transaction_text = str(transaction).replace(',', '\n')
        # Format transaction text for better readability
        formatted_text = self._format_transaction_text(transaction_text)
        self.transaction_display.setText(formatted_text)
        
        main_layout.addWidget(self.transaction_display)
        
        # Mine button
        self.mine_button = QPushButton("Start Mining the blocks")
        self.mine_button.clicked.connect(self.start_mining)
        main_layout.addWidget(self.mine_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def start_mining(self):
        # Switch button function based on text
        if self.mine_button.text() == "EXIT":
            self.exit_to_main()
            return
            
        # Disable button during mining
        self.mine_button.setEnabled(False)
        self.transaction_display.setText("Mining in process...")
        
        # Check for duplicates within the transactions to be mined
        if not self.check_duplicate_transactions_in_block():
            # Proceed with mining
            # Use our own SCRYPT implementation instead of importing from miner
            MinerWindow.blocknumber = MinerWindow.blocknumber + 1
            
            # Set up mining parameters
            difficulty = 2
            prefix_str = '0' * difficulty
            
            # Start mining process
            QApplication.processEvents()  # Update UI
        else:
            # If duplicates found, stop mining and show error
            self.transaction_display.setText("Error: Duplicate transactions detected in block. Mining cancelled.")
            self.mine_button.setText("EXIT")
            self.mine_button.setEnabled(True)
            return
        
        for nonce in range(10000000000):
            mine_string = self.transaction + str(self.last_hash) + str(MinerWindow.blocknumber)
            text = mine_string + str(nonce)
            new_h = self.SCRYPT(text)  # Use the local SCRYPT method
            
            if new_h.startswith(prefix_str):
                print("Successfully mined with nonce:", nonce)
                self.new_hash = new_h
                
                # Check for duplicates in existing blockchain before saving
                if self.check_duplicates_in_blockchain():
                    self.transaction_display.setText("Error: Some transactions are already in the blockchain. Mining cancelled.")
                    self.mine_button.setText("EXIT")
                    self.mine_button.setEnabled(True)
                    MinerWindow.blocknumber -= 1  # Revert block number increase
                    return
                
                # Save to blocks file
                try:
                    file = open("blocks.txt", "a+")
                    file.write("Block number: " + str(MinerWindow.blocknumber) + ", ")
                    file.write("Transactions: {" + self.transaction.replace('\n', ',') + "}, ")
                    file.write("Nonce: " + str(nonce) + ", ")
                    file.write("Number of Transactions: " + str(len(self.original_transactions)) + ", ")
                    file.write("Hash: " + str(new_h) + "\n")
                    file.close()
                except Exception as e:
                    print(f"Error writing to blockchain file: {e}")
                    self.transaction_display.setText(f"Error saving to blockchain: {str(e)}")
                    self.mine_button.setText("EXIT")
                    self.mine_button.setEnabled(True)
                    MinerWindow.blocknumber -= 1  # Revert block number increase
                    return
                
                # Update transaction file by removing all transactions in this block
                for trans in self.original_transactions:
                    if trans in self.parent.transactions:
                        self.parent.transactions.remove(trans)
                
                # Update transaction file
                string = '\n'.join(self.parent.transactions)
                file = open("vehicle_information.txt", "w+")
                file.write(string + "\n" if string else "")
                file.close()
                
                # Update parent's last_hash
                self.parent.last_hash = str(new_h)
                
                # Update UI
                mining_result = "Transaction added to block\n\n"
                mining_result += self.transaction.replace(',', '\n')
                mining_result += "\n\nNONCE: " + str(nonce)
                mining_result += "\nNEW HASH: " + str(new_h)
                self.transaction_display.setText(mining_result)
                
                # Re-enable button with exit text
                self.mine_button.setEnabled(True)
                self.mine_button.setText("EXIT")
                return
                
        # If mining fails
        self.transaction_display.setText("Max limit exceeded")
        self.mine_button.setEnabled(True)
        self.mine_button.setText("EXIT")
        MinerWindow.blocknumber -= 1

    def check_duplicate_transactions_in_block(self):
        """Check if there are duplicate car registrations within the transactions to be mined"""
        car_registrations = []
        
        # Process each transaction in the block
        for transaction in self.original_transactions:
            car_reg = None
            # Extract car registration number
            for part in transaction.split(','):
                if "Car Registration Number:" in part:
                    car_reg = part.strip()
                    break
                    
            if car_reg:
                if car_reg in car_registrations:
                    return True  # Duplicate found
                car_registrations.append(car_reg)
                
        return False  # No duplicates found
        
    def check_duplicates_in_blockchain(self):
        """Check if any transaction in current block already exists in blockchain"""
        if not os.path.exists("blocks.txt"):
            return False
            
        try:
            with open("blocks.txt", "r") as f:
                blockchain_content = f.read()
                
            # Extract all car registration numbers from current transactions
            for transaction in self.original_transactions:
                car_reg = None
                # Extract car registration number
                for part in transaction.split(','):
                    if "Car Registration Number:" in part:
                        car_reg = part.strip()
                        break
                        
                if car_reg and car_reg in blockchain_content:
                    return True  # Found in blockchain
                    
            return False  # No duplicates found
        except Exception:
            # If error reading file, proceed assuming no duplicates
            return False
    
    def _format_transaction_data(self, transaction_text):
        """Format transaction data for better display"""
        return self._format_transaction_text(transaction_text)
        
    def _format_transaction_text(self, transaction_text):
        """Format transaction text for better display with improved readability"""
        # Split by lines
        lines = transaction_text.split('\n')
        formatted_lines = []
        
        for line in lines:
            if ':' in line:
                # Split at the first colon
                parts = line.split(':', 1)
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ""
                # Format key-value pairs for better visibility
                formatted_line = f"{key}: {value}"
                formatted_lines.append(formatted_line)
            else:
                # For lines without colons, just include them as is
                if line.strip():  # Only include non-empty lines
                    formatted_lines.append(line)
                    
        # Join with double line breaks to add more space between entries
        return '\n'.join(formatted_lines)
        
    def SCRYPT(self, text):
        # Implement the SCRYPT method from the original miner class
        import pyscrypt
        salt = os.urandom(8)
        b = bytes(text, 'utf-8')
        digest = pyscrypt.hash(b, salt, 8, 2, 1, 32)
        return str(digest.hex())
        
    def exit_to_main(self):
        self.hide()
        if self.parent and self.parent.parent:
            self.parent.parent.show()


class TransactionEndWindow(QMainWindow):
    def center_on_screen(self):
        # Center window on screen
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.main_parent = parent.parent if parent else None
        
        self.setWindowTitle("Transactions in Blockchain system")
        self.setMinimumSize(500, 300)
        self.center_on_screen()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Check if all transactions have been processed
        if not self.parent.transactions or len(self.parent.transactions) == 0:
            end_label = QLabel("All Transactions Processed")
            end_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 30px 0; color: #006600;")
            message_text = "All transactions have been successfully verified and added to the blockchain!"
        else:
            end_label = QLabel("End of Transactions")
            end_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 30px 0; color: #004080;")
            message_text = "You have reached the end of the transaction list. You can go back to review previous transactions."
            
        end_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(end_label)
        
        # Add additional explanation message
        message_label = QLabel(message_text)
        message_label.setStyleSheet("font-size: 16px; color: #2c3e50; margin-bottom: 20px;")
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setWordWrap(True)
        main_layout.addWidget(message_label)
        
        # Navigation buttons
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        
        # Previous button to go back to transactions
        if self.parent and self.parent.transactions and len(self.parent.transactions) > 0:
            prev_button = QPushButton("Go back to transactions")
            prev_button.clicked.connect(self.go_back_to_transactions)
            buttons_layout.addWidget(prev_button)
        
        # Back button to main menu
        back_button = QPushButton("Go back to Login page")
        back_button.clicked.connect(self.go_back_action)
        buttons_layout.addWidget(back_button)
        
        main_layout.addWidget(buttons_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add additional explanation message
        message_label = QLabel("All transactions have been reviewed. Thank you for your work!")
        message_label.setStyleSheet("font-size: 16px; color: #2c3e50; margin-bottom: 20px;")
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setWordWrap(True)
        main_layout.addWidget(message_label)
        
        # Navigation buttons
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        
        # Previous button to go back to transactions
        prev_button = QPushButton("Go back to transactions")
        prev_button.clicked.connect(self.go_back_to_transactions)
        buttons_layout.addWidget(prev_button)
        
        # Back button to main menu
        back_button = QPushButton("Go back to Login page")
        back_button.clicked.connect(self.go_back_action)
        buttons_layout.addWidget(back_button)
        
        main_layout.addWidget(buttons_widget, alignment=Qt.AlignmentFlag.AlignCenter)

    def go_back_to_transactions(self):
        self.hide()
        if self.parent:
            # Reset the count to the last valid transaction
            self.parent.count = len(self.parent.transactions) - 1 if self.parent.transactions else 0
            if self.parent.transactions:
                # If we still have transactions, show them
                self.parent.transaction_display.setText(str(self.parent.transactions[self.parent.count]).replace(',', '\n'))
                self.parent.prev_button.setEnabled(self.parent.count > 0)
            self.parent.show()
            
    def go_back_action(self):
        self.hide()
        if self.parent:
            self.parent.hide()
        if self.main_parent:
            self.main_parent.show()


class BlocksWindow(QMainWindow):
    def center_on_screen(self):
        # Center window on screen
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        
        self.setWindowTitle("Blocks in System")
        self.setMinimumSize(800, 600)
        self.center_on_screen()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Check for blocks
        if os.path.exists("blocks.txt"):
            f = open("blocks.txt", "r")
            blocks = f.read().split("\n")
            f.close()
            
            # Header
            header_label = QLabel("Blockchain Blocks")
            header_label.setStyleSheet("font-size: 22px; font-weight: bold; margin: 20px 0; color: #00FF00;")
            header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(header_label)
            
            # Create scroll area for blocks
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            
            # Add each block as a styled frame
            for block in blocks:
                if not block:  # Skip empty lines
                    continue
                    
                block_frame = QFrame()
                block_frame.setFrameShape(QFrame.Shape.StyledPanel)
                block_frame.setStyleSheet("""
                    QFrame {
                        background-color: #ecf0f1;
                        border: 1px solid #bdc3c7;
                        border-radius: 5px;
                        margin: 5px;
                    }
                """)
                
                block_layout = QVBoxLayout(block_frame)
                # Format block data for better readability
                formatted_block = self._format_block_text(block)
                block_text = QTextEdit()
                block_text.setReadOnly(True)
                block_text.setHtml(formatted_block)
                block_text.setStyleSheet("""
                    background-color: #f8f9fa;
                    border: 1px solid #d1d1d1;
                    border-radius: 4px;
                    font-family: monospace;
                    font-size: 14px;
                    color: #000000;
                    font-weight: bold;
                    padding: 5px;
                """)
                block_text.setMaximumHeight(120)
                block_layout.addWidget(block_text)
                
                scroll_layout.addWidget(block_frame)
            
            scroll_area.setWidget(scroll_content)
            main_layout.addWidget(scroll_area)
            
        else:
            # No blocks
            no_blocks_label = QLabel("The blockchain does not have any blocks")
            no_blocks_label.setStyleSheet("font-size: 18px; color: #333333; margin: 50px 0;")
            no_blocks_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(no_blocks_label)
        
        # Exit button
        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        exit_button.clicked.connect(self.exit_to_main)
        main_layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def exit_to_main(self):
        self.hide()
        if self.parent:
            self.parent.show()
            
    def _format_block_text(self, block_text):
        """Format block text for better HTML display"""
        # Parse the block text
        html_output = []
        
        # Split by commas and format each part
        parts = block_text.split(',')
        for part in parts:
            if ':' in part:
                key_val = part.split(':', 1)
                key = key_val[0].strip()
                val = key_val[1].strip() if len(key_val) > 1 else ""
                
                # Add HTML formatting - bold for keys, normal for values
                html_output.append(f"<b>{key}:</b> {val}<br>")
            else:
                html_output.append(f"{part}<br>")
                
        return ''.join(html_output)


# Window to display denied transactions
class DeniedTransactionsWindow(QMainWindow):
    def center_on_screen(self):
        # Center window on screen
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        
        self.setWindowTitle("Denied Transactions")
        self.setMinimumSize(800, 600)
        self.center_on_screen()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        header_label = QLabel("Denied Transactions")
        header_label.setStyleSheet("font-size: 22px; font-weight: bold; margin: 20px 0; color: #d32f2f;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Check for denied transactions
        if os.path.exists("denied_transactions.txt"):
            try:
                with open("denied_transactions.txt", "r") as f:
                    content = f.read()
                    denied_transactions = content.split('\n')
                    denied_transactions = [t for t in denied_transactions if t.strip()]
                    
                if denied_transactions:
                    # Create a scroll area for transactions
                    scroll_area = QScrollArea()
                    scroll_area.setWidgetResizable(True)
                    
                    scroll_content = QWidget()
                    scroll_layout = QVBoxLayout(scroll_content)
                    
                    # Display each denied transaction in a card
                    for transaction in denied_transactions:
                        transaction_frame = QFrame()
                        transaction_frame.setFrameShape(QFrame.Shape.StyledPanel)
                        transaction_frame.setStyleSheet("""
                            QFrame {
                                background-color: #ffebee;
                                border: 1px solid #ef9a9a;
                                border-radius: 8px;
                                margin: 5px;
                            }
                        """)
                        
                        transaction_layout = QVBoxLayout(transaction_frame)
                        
                        # Format transaction for display
                        transaction_text = str(transaction).replace(',', '\n')
                        formatted_transaction = self._format_transaction_text(transaction_text)
                        
                        transaction_display = QTextEdit()
                        transaction_display.setReadOnly(True)
                        transaction_display.setText(formatted_transaction)
                        transaction_display.setStyleSheet("""
                            background-color: transparent;
                            border: none;
                            font-family: monospace;
                            font-size: 14px;
                            color: #000000;
                        """)
                        transaction_display.setMaximumHeight(150)
                        
                        transaction_layout.addWidget(transaction_display)
                        scroll_layout.addWidget(transaction_frame)
                    
                    scroll_area.setWidget(scroll_content)
                    main_layout.addWidget(scroll_area)
                else:
                    no_transactions_label = QLabel("No denied transactions found")
                    no_transactions_label.setStyleSheet("font-size: 18px; color: #666666; margin: 50px 0;")
                    no_transactions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    main_layout.addWidget(no_transactions_label)
            except Exception as e:
                error_label = QLabel(f"Error loading denied transactions: {str(e)}")
                error_label.setStyleSheet("font-size: 16px; color: #e74c3c; margin: 50px 0;")
                error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                main_layout.addWidget(error_label)
        else:
            no_file_label = QLabel("No denied transactions have been recorded yet")
            no_file_label.setStyleSheet("font-size: 18px; color: #666666; margin: 50px 0;")
            no_file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(no_file_label)
        
        # Back button
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(self.exit_to_main)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def _format_transaction_text(self, transaction_text):
        """Format transaction text for better display"""
        # Split by lines
        lines = transaction_text.split('\n')
        formatted_lines = []
        
        for line in lines:
            if ':' in line:
                # Split at the first colon
                parts = line.split(':', 1)
                key = parts[0].strip()
                value = parts[1].strip() if len(parts) > 1 else ""
                # Format key-value pairs for better visibility
                formatted_line = f"{key}: {value}"
                formatted_lines.append(formatted_line)
            else:
                # For lines without colons, just include them as is
                if line.strip():  # Only include non-empty lines
                    formatted_lines.append(line)
                    
        # Join with line breaks
        return '\n'.join(formatted_lines)
    
    def exit_to_main(self):
        self.hide()
        if self.parent:
            self.parent.show()


# Enhanced Block class to allow multiple transactions
class Block:
    def __init__(self):
        self.verified_transactions = []  # List to store multiple transactions
        self.previous_block_hash = ""
        self.Nonce = ""
        self.max_transactions = 5  # Maximum number of transactions per block


# Main application entry point
if __name__ == "__main__":
    # Initialize transaction counter from existing data
    CertificateAuthorityWindow.load_transaction_counter()
    
    app = QApplication(sys.argv)
    window = BlockchainApp()
    window.show()
    sys.exit(app.exec())