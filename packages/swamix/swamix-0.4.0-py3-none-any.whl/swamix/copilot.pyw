import sys, time, pyautogui
import io
import sounddevice as sd
import numpy as np
import requests
import json
import os
import base64
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog, QTextEdit
from PySide6.QtCore import Qt, QPoint, QSize, QTimer, QBuffer, QByteArray, QIODevice
from PySide6.QtGui import QIcon, QMouseEvent, QFont, QColor, QClipboard, QPixmap, QScreen
import soundfile as sf
import anthropic
from contextlib import suppress


class ModernWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.dp, self.r, self.ad, self.sr, self.st = QPoint(), 0, [], 44100, None
        self.screen_capture = None
        self.transcription = ""
        self.initUI()

    def initUI(self):
        self.setStyleSheet(
            """
            QWidget#mainWidget {
                background-color: #1a1a1a;
                border-radius: 10px;
                border: 1px solid #333;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border: none;
                padding: 15px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px;
                border-radius: 10px;
                min-width: 100px;
                min-height: 100px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton#closeButton {
                background-color: transparent;
                color: #cccccc; 
                min-width: 30px;
                min-height: 30px;
                font-size: 20px;
                border-radius: 15px;
                padding: 0px;
                margin: 0px;
            }
            QPushButton#closeButton:hover {
                background-color: #ff4444;
                color: white;
            }
            """
        )

        main_widget = QWidget(self)
        main_widget.setObjectName("mainWidget")

        # Main container layout
        container_layout = QVBoxLayout(main_widget)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Top bar with close button
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(10, 10, 10, 0)

        title_label = QLabel("Swamix Copilot")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")

        close_button = QPushButton("×")
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.close)

        top_bar.addWidget(title_label)
        top_bar.addStretch()
        top_bar.addWidget(close_button)

        # Main content area
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 10, 20, 20)
        content_layout.setSpacing(20)

        # Left side
        left_layout = QVBoxLayout()

        self.screen_view = QLabel()
        self.screen_view.setFixedSize(320, 180)  # 16:9 aspect ratio
        self.screen_view.setStyleSheet(
            """
            border: 1px solid #444; 
            border-radius: 5px;
            background-color: #2d2d2d;
        """
        )
        left_layout.addWidget(self.screen_view)

        self.status_label = QLabel("Ready to record")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #999; margin-top: 10px;")
        self.status_label.setWordWrap(True)
        left_layout.addWidget(self.status_label)

        left_layout.addStretch(1)

        # Right side - Button Grid
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)

        grid_layout = QVBoxLayout()
        grid_layout.setSpacing(10)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(10)

        # Configure buttons with SVG icons
        self.rb = QPushButton()
        self.rb.setIcon(
            QIcon(
                """
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 15C13.66 15 15 13.66 15 12V6C15 4.34 13.66 3 12 3C10.34 3 9 4.34 9 6V12C9 13.66 10.34 15 12 15Z" fill="currentColor"/>
                <path d="M17 12C17 14.76 14.76 17 12 17C9.24 17 7 14.76 7 12H5C5 15.53 7.61 18.43 11 18.92V21H13V18.92C16.39 18.43 19 15.53 19 12H17Z" fill="currentColor"/>
            </svg>
        """
            )
        )
        self.rb.setIconSize(QSize(32, 32))
        self.rb.clicked.connect(self.tr)

        self.type_button = QPushButton()
        self.type_button.setIcon(
            QIcon(
                """
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 5H4V7H20V5ZM20 9H4V11H20V9ZM20 13H4V15H20V13ZM20 17H4V19H20V17Z" fill="currentColor"/>
            </svg>
        """
            )
        )
        self.type_button.setIconSize(QSize(32, 32))
        self.type_button.clicked.connect(self.type_copied_text)

        self.capture_button = QPushButton()
        self.capture_button.setIcon(
            QIcon(
                """
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 15.2C13.7674 15.2 15.2 13.7674 15.2 12C15.2 10.2326 13.7674 8.8 12 8.8C10.2326 8.8 8.8 10.2326 8.8 12C8.8 13.7674 10.2326 15.2 12 15.2Z" fill="currentColor"/>
                <path d="M9 3L7.17 5H4C2.9 5 2 5.9 2 7V19C2 20.1 2.9 21 4 21H20C21.1 21 22 20.1 22 19V7C22 5.9 21.1 5 20 5H16.83L15 3H9ZM12 17C9.24 17 7 14.76 7 12C7 9.24 9.24 7 12 7C14.76 7 17 9.24 17 12C17 14.76 14.76 17 12 17Z" fill="currentColor"/>
            </svg>
        """
            )
        )
        self.capture_button.setIconSize(QSize(32, 32))
        self.capture_button.clicked.connect(self.capture_screen)

        self.send_button = QPushButton()
        self.send_button.setIcon(
            QIcon(
                """
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M2.01 21L23 12L2.01 3L2 10L17 12L2 14L2.01 21Z" fill="currentColor"/>
            </svg>
        """
            )
        )
        self.send_button.setIconSize(QSize(32, 32))
        self.send_button.clicked.connect(self.send_to_claude)

        # Add tooltips
        self.rb.setToolTip("Record Audio")
        self.type_button.setToolTip("Type Text")
        self.capture_button.setToolTip("Capture Screen")
        self.send_button.setToolTip("Send to Claude")

        # Add buttons to grid
        for btn in [self.rb, self.type_button]:
            btn.setFixedSize(100, 100)
            top_row.addWidget(btn)

        for btn in [self.capture_button, self.send_button]:
            btn.setFixedSize(100, 100)
            bottom_row.addWidget(btn)

        grid_layout.addLayout(top_row)
        grid_layout.addLayout(bottom_row)

        right_layout.addLayout(grid_layout)
        right_layout.addStretch(1)

        # Add layouts to content area
        content_layout.addLayout(left_layout, 2)
        content_layout.addLayout(right_layout, 1)

        # Add all layouts to container
        container_layout.addLayout(top_bar)
        container_layout.addLayout(content_layout)

        # Set up outer layout
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(main_widget)

        self.setMinimumSize(600, 400)
        # self.resize(self.sizeHint())
        self.setWindowTitle('Swamix Copilot')
        self.show()

    def sizeHint(self):
        return QSize(600, 400)

    def type_copied_text(self):
        time.sleep(3)
        pyautogui.typewrite(QApplication.clipboard().text())

    def tr(self):
        if not self.r:
            self.r = 1
            self.rb.setText("Stop Recording")
            self.rb.setStyleSheet("background-color: #f44336;")
            self.status_label.setText("Recording...")
            self.ad = []
            self.st = sd.InputStream(callback=self.ac, channels=1, samplerate=self.sr)
            self.st.start()
        else:
            self.r = 0
            self.rb.setText("Record Audio")
            self.rb.setStyleSheet("background-color: #4CAF50;")
            self.status_label.setText("Processing...")
            self.st and (self.st.stop(), self.st.close())
            self.pa()

    def ac(self, i, f, t, st):
        st and print(st)
        self.r and self.ad.append(i.copy())

    def pa(self):
        if not self.ad:
            self.status_label.setText("No audio data recorded")
            return
        audio_data = np.concatenate(self.ad, axis=0)
        audio_buffer = io.BytesIO()
        sf.write(audio_buffer, audio_data, self.sr, format='wav')
        audio_buffer.seek(0)
        self.transcribe_audio(audio_buffer)

    def transcribe_audio(self, af):
        self.status_label.setText("Transcribing...")
        r = requests.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"},
            files={"file": ("audio.wav", af, "audio/wav")},
            data={"model": "whisper-large-v3-turbo", "temperature": 0, "response_format": "json", "language": "en"},
        )
        result = r.json()['text'] if r.status_code == 200 else f"Error:{r.status_code} {r.text}"
        self.transcription = result
        self.status_label.setText(f"Transcription: {result}")
        print("Transcription:", result)
        QApplication.clipboard().setText(result)
        self.status_label.setText(f"Transcription copied to clipboard: {result}")

    def capture_screen(self):
        screen = QApplication.primaryScreen()
        self.screen_capture = screen.grabWindow(0)
        scaled_pixmap = self.screen_capture.scaled(self.screen_view.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.screen_view.setPixmap(scaled_pixmap)
        self.status_label.setText("Screen captured")

    def send_to_claude(self):
        try:
            # Validate inputs
            if not self.screen_capture and not self.transcription:
                self.status_label.setText("Error: Please provide either an image or voiceover")
                return

            self.status_label.setText("Sending to Claude...")

            # Convert QPixmap to base64-encoded string if screen capture exists
            image_base64 = None
            if self.screen_capture:
                try:
                    buffer = QByteArray()
                    buffer_io = QBuffer(buffer)
                    buffer_io.open(QIODevice.OpenModeFlag.WriteOnly)
                    with suppress(Exception):
                        self.screen_capture.save(buffer_io, "PNG")

                    image_base64 = buffer.toBase64().toStdString()
                    # print("Image base64:", image_base64)
                except Exception as e:
                    self.status_label.setText(f"Error processing image: {str(e)}")
                    return
                finally:
                    buffer_io.close()

            # Validate API key
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                self.status_label.setText("Error: ANTHROPIC_API_KEY not found in environment variables")
                return

            # Create Anthropic client
            client = anthropic.Anthropic(api_key=api_key)

            # Prepare the system prompt
            system_prompt = f"""
            # Task
            you are an interview engine, and i will input vocally, give very short answer to satisfy my query
            your objective to just answer, or draft a verbal reply, to impress interviewer (software interview)

            # Voice Transcript by user are
            {self.transcription}
            """

            # Build message content
            messages = []
            # Add image message if image exists
            if image_base64:
                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Use this as reference"},
                            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_base64}},
                        ],
                    }
                )

            # Add main message
            messages.append({"role": "user", "content": f"Please answer based on transcript{' and image' if image_base64 else ''}."})
            print("Messages:", messages)
            # Send request to Claude
            try:
                response = client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1024,
                    temperature=0.7,
                    system=system_prompt,
                    messages=messages,
                )

                claude_response = response.content[0].text
                self.show_claude_response(claude_response)

                # Copy response to clipboard
                clipboard = QApplication.clipboard()
                clipboard.setText(claude_response)
                self.status_label.setText("Response received and copied to clipboard")

            except anthropic.APIError as api_error:
                self.status_label.setText(f"Claude API Error: {str(api_error)}")
            except anthropic.RateLimitError:
                self.status_label.setText("Rate limit exceeded. Please wait before trying again")
            except anthropic.APIConnectionError:
                self.status_label.setText("Connection error. Please check your internet connection")
            except Exception as e:
                self.status_label.setText(f"Unexpected error while calling Claude: {str(e)}")

        except Exception as e:
            self.status_label.setText(f"Critical error: {str(e)}")

    def show_claude_response(self, response):
        dialog = QDialog(self)
        dialog.setWindowTitle("Claude's Response")
        layout = QVBoxLayout(dialog)

        text_edit = QTextEdit()
        text_edit.setPlainText(response)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)

        copy_button = QPushButton("Copy to Clipboard")
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(response))
        layout.addWidget(copy_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.resize(500, 400)
        dialog.exec()

    def copy_to_clipboard(self, text):
        QApplication.clipboard().setText(text)
        self.status_label.setText("Response copied to clipboard")

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.MouseButton.LeftButton:
            self.dp = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
            e.accept()

    def mouseMoveEvent(self, e: QMouseEvent):
        if e.buttons() & Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self.dp)
            e.accept()

    def mouseReleaseEvent(self, e: QMouseEvent):
        self.dp = QPoint()
        e.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernWidget()
    sys.exit(app.exec())
