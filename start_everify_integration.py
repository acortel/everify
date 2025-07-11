#!/usr/bin/env python3
"""
Startup Script for eVerify Integration
Launches Flask server and desktop application with proper configuration.
"""

import subprocess
import time
import sys
import os
import requests
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QMessageBox
from PySide6.QtCore import QTimer

class StartupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("eVerify Integration Startup")
        self.setGeometry(100, 100, 500, 400)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Add title
        title = QLabel("eVerify Integration Startup")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px; color: #333;")
        layout.addWidget(title)
        
        # Status labels
        self.flask_status = QLabel("🔴 Flask Server: Not Running")
        self.flask_status.setStyleSheet("font-size: 14px; margin: 10px; padding: 10px; background-color: #f8d7da; border-radius: 5px;")
        layout.addWidget(self.flask_status)
        
        self.app_status = QLabel("🔴 Desktop App: Not Started")
        self.app_status.setStyleSheet("font-size: 14px; margin: 10px; padding: 10px; background-color: #f8d7da; border-radius: 5px;")
        layout.addWidget(self.app_status)
        
        # Buttons
        self.start_flask_btn = QPushButton("🚀 Start Flask Server")
        self.start_flask_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        self.start_flask_btn.clicked.connect(self.start_flask_server)
        layout.addWidget(self.start_flask_btn)
        
        self.start_app_btn = QPushButton("🚀 Start Desktop App")
        self.start_app_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        self.start_app_btn.clicked.connect(self.start_desktop_app)
        self.start_app_btn.setEnabled(False)  # Disabled until Flask is running
        layout.addWidget(self.start_app_btn)
        
        # Auto-start button
        self.auto_start_btn = QPushButton("⚡ Auto-Start Everything")
        self.auto_start_btn.setStyleSheet("""
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
        """)
        self.auto_start_btn.clicked.connect(self.auto_start_everything)
        layout.addWidget(self.auto_start_btn)
        
        # Timer to check Flask server status
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.check_flask_status)
        self.status_timer.start(2000)  # Check every 2 seconds
        
        # Store processes
        self.flask_process = None
        self.app_process = None
        
    def check_flask_status(self):
        """Check if Flask server is running."""
        try:
            response = requests.get("http://127.0.0.1:5000/liveness", timeout=2)
            if response.status_code == 200:
                self.flask_status.setText("🟢 Flask Server: Running")
                self.flask_status.setStyleSheet("font-size: 14px; margin: 10px; padding: 10px; background-color: #d4edda; border-radius: 5px; color: #155724;")
                self.start_app_btn.setEnabled(True)
                return True
            else:
                self.flask_status.setText("🔴 Flask Server: Not Responding")
                self.flask_status.setStyleSheet("font-size: 14px; margin: 10px; padding: 10px; background-color: #f8d7da; border-radius: 5px; color: #721c24;")
                self.start_app_btn.setEnabled(False)
                return False
        except:
            self.flask_status.setText("🔴 Flask Server: Not Running")
            self.flask_status.setStyleSheet("font-size: 14px; margin: 10px; padding: 10px; background-color: #f8d7da; border-radius: 5px; color: #721c24;")
            self.start_app_btn.setEnabled(False)
            return False
    
    def start_flask_server(self):
        """Start the Flask server for face liveness."""
        try:
            flask_path = "flask_server/app.py"
            if not os.path.exists(flask_path):
                QMessageBox.critical(self, "Error", 
                                   f"Flask server not found at: {flask_path}\n\n"
                                   "Please ensure the flask_server directory exists.")
                return
            
            self.flask_process = subprocess.Popen([
                sys.executable, flask_path
            ])
            
            self.start_flask_btn.setText("⏳ Starting Flask Server...")
            self.start_flask_btn.setEnabled(False)
            
            print("✅ Flask server starting...")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start Flask server: {str(e)}")
    
    def start_desktop_app(self):
        """Start the desktop application."""
        try:
            app_path = "example_desktop_app.py"
            if not os.path.exists(app_path):
                QMessageBox.critical(self, "Error", 
                                   f"Desktop app not found at: {app_path}\n\n"
                                   "Please ensure the example_desktop_app.py file exists.")
                return
            
            self.app_process = subprocess.Popen([
                sys.executable, app_path
            ])
            
            self.start_app_btn.setText("⏳ Desktop App Running...")
            self.start_app_btn.setEnabled(False)
            
            self.app_status.setText("🟢 Desktop App: Running")
            self.app_status.setStyleSheet("font-size: 14px; margin: 10px; padding: 10px; background-color: #d4edda; border-radius: 5px; color: #155724;")
            
            print("✅ Desktop app started successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start desktop app: {str(e)}")
    
    def auto_start_everything(self):
        """Automatically start both Flask server and desktop app."""
        self.auto_start_btn.setText("⏳ Starting Everything...")
        self.auto_start_btn.setEnabled(False)
        
        # Start Flask server first
        self.start_flask_server()
        
        # Wait a bit, then start desktop app
        QTimer.singleShot(5000, self.start_desktop_app)
    
    def closeEvent(self, event):
        """Clean up processes when closing."""
        if self.flask_process:
            try:
                self.flask_process.terminate()
                print("🛑 Flask server stopped")
            except:
                pass
        
        if self.app_process:
            try:
                self.app_process.terminate()
                print("🛑 Desktop app stopped")
            except:
                pass
        
        event.accept()

def main():
    """Main function to run the startup window."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the startup window
    window = StartupWindow()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 