#!/usr/bin/env python3
"""
Example Desktop Application with eVerify Integration
"""

import sys
import subprocess
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class DesktopAppWithEVerify(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Your Desktop App with eVerify")
        self.setGeometry(100, 100, 600, 400)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Add title
        title = QLabel("Your Desktop Application")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px; color: #333;")
        layout.addWidget(title)
        
        # Add eVerify button
        self.everify_button = QPushButton("🔍 Launch eVerify")
        self.everify_button.setStyleSheet("""
            QPushButton {
                background-color: #ce305e;
                color: white;
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #e0446a;
            }
            QPushButton:pressed {
                background-color: #b02a4e;
            }
        """)
        self.everify_button.clicked.connect(self.launch_everify)
        layout.addWidget(self.everify_button)
        
        # Add result display area
        self.result_group = QGroupBox("eVerify Results")
        self.result_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        result_layout = QVBoxLayout()
        self.result_group.setLayout(result_layout)
        
        self.result_label = QLabel("No verification result yet")
        self.result_label.setStyleSheet("""
            margin: 10px; 
            padding: 15px; 
            background-color: #f8f9fa; 
            border-radius: 5px; 
            border: 1px solid #dee2e6;
        """)
        result_layout.addWidget(self.result_label)
        
        layout.addWidget(self.result_group)
        
        # Add other app functionality
        self.add_other_functionality(layout)
        
        # Timer to check for eVerify results
        self.result_timer = QTimer()
        self.result_timer.timeout.connect(self.check_everify_result)
        self.everify_process = None
        
    def add_other_functionality(self, layout):
        """Add other functionality to your app."""
        
        # Example: Add some other buttons/features
        other_group = QGroupBox("Other App Features")
        other_layout = QHBoxLayout()
        other_group.setLayout(other_layout)
        
        # Example buttons
        btn1 = QPushButton("Feature 1")
        btn2 = QPushButton("Feature 2")
        btn3 = QPushButton("Feature 3")
        
        for btn in [btn1, btn2, btn3]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #6c757d;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    margin: 5px;
                }
                QPushButton:hover {
                    background-color: #5a6268;
                }
            """)
            other_layout.addWidget(btn)
        
        layout.addWidget(other_group)
        
    def launch_everify(self):
        """Launch the eVerify standalone application."""
        try:
            # First, check if Flask server is running (required for face liveness)
            if not self.check_flask_server():
                QMessageBox.critical(self, "Flask Server Required", 
                                   "The Flask server is not running.\n\n"
                                   "Face liveness check requires the Flask server to be running.\n"
                                   "Please start the Flask server first:\n"
                                   "python flask_server/app.py")
                return
            
            # Path to your eVerify standalone package
            everify_path = "everify_standalone_package/everify_standalone.py"
            
            # Check if the file exists
            if not os.path.exists(everify_path):
                QMessageBox.critical(self, "Error", 
                                   f"eVerify application not found at: {everify_path}\n\n"
                                   "Please run package_everify.py first to create the package.")
                return
            
            # Launch eVerify as a separate process
            self.everify_process = subprocess.Popen([
                sys.executable, everify_path
            ])
            
            # Start timer to check for completion
            self.result_timer.start(2000)  # Check every 2 seconds
            
            self.everify_button.setText("⏳ eVerify Running...")
            self.everify_button.setEnabled(False)
            
            print("✅ eVerify launched successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to launch eVerify: {str(e)}")
    
    def check_flask_server(self):
        """Check if Flask server is running for face liveness."""
        try:
            import requests
            response = requests.get("http://127.0.0.1:5000/liveness", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def check_everify_result(self):
        """Check if eVerify has completed."""
        if self.everify_process:
            # Check if the process is still running
            if self.everify_process.poll() is not None:
                # Process has finished
                self.result_timer.stop()
                self.everify_button.setText("🔍 Launch eVerify")
                self.everify_button.setEnabled(True)
                self.everify_process = None
                
                # Check database for recent verification
                self.check_database_for_results()
    
    def check_database_for_results(self):
        """Check database for recent verification results."""
        try:
            import psycopg2
            from datetime import datetime, timedelta
            
            # Connect to database
            conn = psycopg2.connect(
                host=os.getenv('PGHOST', 'localhost'),
                port=os.getenv('PGPORT', '5432'),
                user=os.getenv('PGUSER', 'postgres'),
                password=os.getenv('PGPASSWORD', ''),
                dbname=os.getenv('PGDATABASE', 'your_project_verifications')
            )
            
            cursor = conn.cursor()
            
            # Get the most recent verification (last 5 minutes)
            five_minutes_ago = datetime.now() - timedelta(minutes=5)
            
            cursor.execute("""
                SELECT first_name, last_name, gender, marital_status, created_at
                FROM verifications 
                WHERE created_at > %s
                ORDER BY created_at DESC 
                LIMIT 1
            """, (five_minutes_ago,))
            
            result = cursor.fetchone()
            
            if result:
                first_name, last_name, gender, marital_status, created_at = result
                
                # Build full name based on gender and marital status
                if gender == 'Female' and marital_status == "Married":
                    full_name = f"{first_name} {last_name}"
                else:
                    full_name = f"{first_name} {last_name}"
                
                # Update UI with result
                self.result_label.setText(
                    f"✅ Verification Successful!\n\n"
                    f"Name: {full_name}\n"
                    f"Gender: {gender}\n"
                    f"Marital Status: {marital_status}\n"
                    f"Verified at: {created_at.strftime('%Y-%m-%d %H:%M:%S')}"
                )
                self.result_label.setStyleSheet("""
                    margin: 10px; 
                    padding: 15px; 
                    background-color: #d4edda; 
                    border-radius: 5px; 
                    color: #155724;
                    border: 1px solid #c3e6cb;
                """)
                
                # You can now use this data in your application
                self.handle_verification_result(full_name, {
                    'first_name': first_name,
                    'last_name': last_name,
                    'gender': gender,
                    'marital_status': marital_status,
                    'verified_at': created_at
                })
                
            else:
                self.result_label.setText("❌ No recent verification found")
                self.result_label.setStyleSheet("""
                    margin: 10px; 
                    padding: 15px; 
                    background-color: #f8d7da; 
                    border-radius: 5px; 
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                """)
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Error checking database: {e}")
            self.result_label.setText(f"❌ Error checking results: {str(e)}")
    
    def handle_verification_result(self, full_name, verification_data):
        """Handle the verification result in your application."""
        print(f"📝 Processing verification result for: {full_name}")
        print(f"Verification data: {verification_data}")
        
        # Example: Update your application's state
        # - Update database records
        # - Enable certain features
        # - Update UI elements
        # - Send notifications
        # - etc.
        
        QMessageBox.information(self, "Verification Complete", 
                              f"Successfully verified: {full_name}\n\n"
                              "The verification data has been integrated into your application.")

def main():
    """Main function to run the desktop application."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the app
    window = DesktopAppWithEVerify()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 