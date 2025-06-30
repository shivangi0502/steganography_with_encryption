from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QLineEdit, QTextEdit, QFileDialog, 
    QStackedWidget, QFrame
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from src.steganography import Steganography
import os

class InstaStegGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("InstaSteg")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fafafa;
            }
            QPushButton {
                background-color: #0095f6;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0080e5;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #dbdbdb;
                border-radius: 4px;
                padding: 8px;
            }
            QLabel {
                color: #262626;
            }
            .header {
                background-color: white;
                border-bottom: 1px solid #dbdbdb;
            }
            .image_container {
                border: 1px solid #dbdbdb;
                background-color: white;
                border-radius: 4px;
            }
        """)
        
        self.current_image_path = None
        self.init_ui()
        
    def init_ui(self):
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Header
        self.header = QWidget()
        self.header.setFixedHeight(60)
        self.header.setObjectName("header")
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        self.logo_label = QLabel("InstaSteg")
        self.logo_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_layout.addWidget(self.logo_label)
        header_layout.addStretch()
        
        self.main_layout.addWidget(self.header)
        
        # Main content area
        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack)
        
        # Home page
        self.home_page = QWidget()
        self.setup_home_page()
        self.content_stack.addWidget(self.home_page)
        
        # Set home as default page
        self.content_stack.setCurrentWidget(self.home_page)
        
    def setup_home_page(self):
        layout = QVBoxLayout(self.home_page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        # Image display area
        self.image_frame = QFrame()
        self.image_frame.setObjectName("image_container")
        self.image_frame.setFixedSize(400, 400)
        self.image_frame.setLayout(QVBoxLayout())
        self.image_frame.layout().setAlignment(Qt.AlignCenter)
        
        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_frame.layout().addWidget(self.image_label)
        
        layout.addWidget(self.image_frame, 0, Qt.AlignCenter)
        
        # Load image button
        self.load_image_btn = QPushButton("Load Image")
        self.load_image_btn.setFixedWidth(200)
        self.load_image_btn.clicked.connect(self.load_image)
        layout.addWidget(self.load_image_btn, 0, Qt.AlignCenter)
        
        # Message input
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Enter your secret message here...")
        self.message_input.setFixedHeight(100)
        layout.addWidget(QLabel("Secret Message:"))
        layout.addWidget(self.message_input)
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        
        # Buttons row
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        
        self.encode_btn = QPushButton("Encode Message")
        self.encode_btn.setFixedWidth(180)
        self.encode_btn.clicked.connect(self.encode_message)
        buttons_layout.addWidget(self.encode_btn)
        
        self.decode_btn = QPushButton("Decode Message")
        self.decode_btn.setFixedWidth(180)
        self.decode_btn.clicked.connect(self.decode_message)
        buttons_layout.addWidget(self.decode_btn)
        
        layout.addLayout(buttons_layout)
        
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        
        if file_path:
            self.current_image_path = file_path
            pixmap = QPixmap(file_path)
            
            # Scale the image to fit while maintaining aspect ratio
            if pixmap.width() > 400 or pixmap.height() > 400:
                pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            self.image_label.setPixmap(pixmap)
            
    def encode_message(self):
        if not self.current_image_path:
            self.show_error("Please load an image first")
            return
            
        message = self.message_input.toPlainText()
        password = self.password_input.text()
        
        if not message:
            self.show_error("Please enter a message to encode")
            return
            
        if not password:
            self.show_error("Please enter a password")
            return
            
        # Get output path
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Save Encoded Image", "", "PNG Image (*.png)")
            
        if output_path:
            success, result = Steganography.encode_message(
                self.current_image_path, message, password, output_path)
                
            if success:
                self.show_success(result)
            else:
                self.show_error(result)
                
    def decode_message(self):
        if not self.current_image_path:
            self.show_error("Please load an image first")
            return
            
        password = self.password_input.text()
        
        if not password:
            self.show_error("Please enter the password")
            return
            
        success, result = Steganography.decode_message(
            self.current_image_path, password)
            
        if success:
            self.message_input.setPlainText(result)
            self.show_success("Message decoded successfully!")
        else:
            self.show_error(result)
            
    def show_error(self, message):
        error_label = QLabel(message)
        error_label.setStyleSheet("color: red;")
        error_label.setAlignment(Qt.AlignCenter)
        
        temp_widget = QWidget()
        layout = QVBoxLayout(temp_widget)
        layout.addWidget(error_label)
        
        self.content_stack.addWidget(temp_widget)
        self.content_stack.setCurrentWidget(temp_widget)
        
        QTimer.singleShot(3000, lambda: self.content_stack.setCurrentWidget(self.home_page))
        
    def show_success(self, message):
        success_label = QLabel(message)
        success_label.setStyleSheet("color: green;")
        success_label.setAlignment(Qt.AlignCenter)
        
        temp_widget = QWidget()
        layout = QVBoxLayout(temp_widget)
        layout.addWidget(success_label)
        
        self.content_stack.addWidget(temp_widget)
        self.content_stack.setCurrentWidget(temp_widget)
        
        QTimer.singleShot(3000, lambda: self.content_stack.setCurrentWidget(self.home_page))
