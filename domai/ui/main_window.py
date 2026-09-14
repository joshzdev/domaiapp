"""
DōmAI UI - Main Window
Modern UI implementation for the security assistant
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QLineEdit, QPushButton, QLabel,
    QComboBox, QFrame, QScrollArea, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
import asyncio
import sys
import json
from pathlib import Path

from ..main import DomAI
from ..ai.model_config import ModelProvider

# Available models by provider
MODELS = {
    "OpenAI": [
        "gpt-4-turbo-preview",
        "gpt-4",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k"
    ],
    "Google": [
        "gemini-pro",
        "gemini-pro-vision"
    ],
    "Mistral": [
        "mistral-tiny",
        "mistral-small",
        "mistral-medium",
        "mistral-large-latest"
    ]
}

class AsyncWorker(QThread):
    """Async worker for handling LLM requests"""
    finished = pyqtSignal(tuple)
    
    def __init__(self, app, query):
        super().__init__()
        self.app = app
        self.query = query
        
    def run(self):
        """Run async task in thread"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            self.app.process_query(self.query)
        )
        loop.close()
        self.finished.emit(result)

class ResponseWidget(QFrame):
    """Custom widget for displaying responses"""
    
    def __init__(self, title: str, icon: str):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        
        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Header
        header = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("", 20))
        title_label = QLabel(title)
        title_label.setFont(QFont("", 12, QFont.Weight.Bold))
        header.addWidget(icon_label)
        header.addWidget(title_label)
        header.addStretch()
        
        # Content
        self.content = QTextEdit()
        self.content.setReadOnly(True)
        self.content.setMinimumHeight(200)
        
        # Add to layout
        layout.addLayout(header)
        layout.addWidget(self.content)
        
    def set_text(self, text: str):
        """Set response text"""
        self.content.setText(text)
        
    def clear(self):
        """Clear response"""
        self.content.clear()

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.app = DomAI()
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI components"""
        self.setWindowTitle("DōmAI - MacOS Security Assistant")
        self.setMinimumSize(800, 600)
        
        # Create central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        layout = QVBoxLayout()
        central.setLayout(layout)
        
        # Model selection
        model_layout = QHBoxLayout()
        
        # Provider selection
        provider_label = QLabel("Provider:")
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(list(MODELS.keys()))
        self.provider_combo.currentTextChanged.connect(self._update_models)
        
        # Model selection
        model_label = QLabel("Model:")
        self.model_combo = QComboBox()
        self._update_models(self.provider_combo.currentText())
        
        model_layout.addWidget(provider_label)
        model_layout.addWidget(self.provider_combo)
        model_layout.addSpacing(20)
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        model_layout.addStretch()
        
        # Response area
        responses = QSplitter(Qt.Orientation.Horizontal)
        
        # Security response
        self.security_response = ResponseWidget("Security Response", "🔒")
        
        # Educational content
        self.educational_content = ResponseWidget("Learn More", "📚")
        
        responses.addWidget(self.security_response)
        responses.addWidget(self.educational_content)
        responses.setSizes([400, 400])
        
        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask me about MacOS security...")
        self.input_field.returnPressed.connect(self.process_input)
        
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.process_input)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        
        # Add everything to main layout
        layout.addLayout(model_layout)
        layout.addWidget(responses)
        layout.addLayout(input_layout)
        
        # Apply styling
        self.apply_styling()
        
    def _update_models(self, provider: str):
        """Update model list based on selected provider"""
        self.model_combo.clear()
        self.model_combo.addItems(MODELS[provider])
        
    def _get_selected_provider(self) -> ModelProvider:
        """Get selected provider enum"""
        provider_text = self.provider_combo.currentText().upper()
        return ModelProvider[provider_text]
        
    def apply_styling(self):
        """Apply modern styling to UI"""
        # Set dark theme
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        
        self.setPalette(palette)
        
        # Style sheets
        self.setStyleSheet("""
            QMainWindow {
                background-color: #353535;
            }
            QFrame {
                background-color: #2b2b2b;
                border-radius: 5px;
                padding: 10px;
            }
            QTextEdit {
                background-color: #1e1e1e;
                border: none;
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #1e1e1e;
                border: none;
                border-radius: 3px;
                padding: 8px;
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QComboBox {
                background-color: #1e1e1e;
                border: none;
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
                min-width: 150px;
            }
            QLabel {
                color: #ffffff;
            }
        """)
        
    def process_input(self):
        """Process user input"""
        query = self.input_field.text().strip()
        if not query:
            return
            
        # Clear input
        self.input_field.clear()
        
        # Disable input during processing
        self.input_field.setEnabled(False)
        self.send_button.setEnabled(False)
        
        # Show processing state
        self.security_response.set_text("Processing security response...")
        self.educational_content.set_text("Waiting for security analysis...")
        
        # Update app configuration
        provider = self._get_selected_provider()
        model_id = self.model_combo.currentText()
        self.app.config_manager.update_config(
            provider,
            model_id=model_id
        )
        
        # Process in background
        self.worker = AsyncWorker(self.app, query)
        self.worker.finished.connect(self.handle_response)
        self.worker.start()
        
    def handle_response(self, result):
        """Handle response from worker"""
        crisis, knowledge = result
        
        # Update security response immediately
        self.security_response.set_text(crisis)
        
        # Show processing state for educational content
        self.educational_content.set_text("Analyzing security response and preparing educational content...")
        
        # Add slight delay before showing educational content
        def show_educational():
            self.educational_content.set_text(knowledge)
            
        QThread.msleep(1500)  # 1.5 second delay
        show_educational()
        
        # Re-enable input
        self.input_field.setEnabled(True)
        self.send_button.setEnabled(True)
        self.input_field.setFocus()

def launch_ui():
    """Launch the UI application"""
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 