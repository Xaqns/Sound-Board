import sys
import os
import shutil
import QtQuick 2.0
import QtQuick.Particles 2.0
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QGridLayout, QSizePolicy, QSpacerItem, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from pygame import mixer
from time import sleep

class SoundboardApp(QWidget):
    def __init__(self):
        super().__init__()
        self.sounds_dir = 'sounds'
        os.system("cls")
        os.makedirs(self.sounds_dir, exist_ok=True)
        print("Sound dir loaded")
        self.initUI()
        print("UI Loaded")
        self.load_sounds()
        print("Sounds Loaded")
        print("  ")
        
    def initUI(self):
        self.layout = QVBoxLayout()

        self.title = QLabel('Xaqns Soundboard')
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFont(QFont('Arial', 24, QFont.Bold))
        self.title.setStyleSheet('color: white;')
        self.layout.addWidget(self.title)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)
        
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.button_layout = QHBoxLayout()
        self.load_button = QPushButton('Load Sound', self)
        self.load_button.setFixedSize(150, 50)  
        self.load_button.clicked.connect(self.load_sound)
        self.button_layout.addWidget(self.load_button, 0, Qt.AlignHCenter)
        
        self.layout.addLayout(self.button_layout)
        
        self.setLayout(self.layout)
        
        self.setWindowTitle('Xaqns Soundboard App')
        self.show()
        
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('#2c3e50'))
        self.setPalette(palette)
        
        mixer.init()
        self.sounds = []
        self.button_size = 100
        self.row = 0
        self.col = 0
        
        self.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                background-color: #3498db; /* Blue background */
                color: white; /* White text */
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980b9; /* Darker blue */
            }
        """)
        
    def load_sound(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Sound File", "", "Audio Files (*.wav *.mp3)", options=options)
        if file_name:
            dest_file = os.path.join(self.sounds_dir, os.path.basename(file_name))
            shutil.copyfile(file_name, dest_file)
            self.add_sound_button(dest_file)
        
    def add_sound_button(self, file_name):
        sound_button_layout = QVBoxLayout()
        
        sound_button = QPushButton(os.path.basename(file_name), self)
        sound_button.setFixedSize(self.button_size, self.button_size)
        sound_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sound_button.clicked.connect(lambda: self.play_sound(file_name, sound_button))
        
        sound_button_layout.addWidget(sound_button)

        button_controls_layout = QHBoxLayout()

        edit_button = QPushButton('Edit', self)
        edit_button.setFixedSize(self.button_size // 2, 30)
        edit_button.clicked.connect(lambda: self.edit_sound_name(file_name, sound_button))

        delete_button = QPushButton('Delete', self)
        delete_button.setFixedSize(self.button_size // 2, 30)
        delete_button.clicked.connect(lambda: self.delete_sound(file_name, sound_button_layout))

        button_controls_layout.addWidget(edit_button)
        button_controls_layout.addWidget(delete_button)
        
        sound_button_layout.addLayout(button_controls_layout)
        
        self.grid_layout.addLayout(sound_button_layout, self.row, self.col)
        
        self.col += 1
        if self.col >= 3:
            self.col = 0
            self.row += 1
            
        self.sounds.append(file_name)
        
    def play_sound(self, file_name, button):
        self.animate_button(button)
        
        mixer.music.load(file_name)
        mixer.music.play()
        print(f"Played: {file_name}")
    
    def animate_button(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        original_geometry = button.geometry()
        shrink_geometry = QRect(original_geometry.x() + 5, original_geometry.y() + 5, original_geometry.width() - 10, original_geometry.height() - 10)
        
        animation.setDuration(100)
        animation.setKeyValueAt(0, original_geometry)
        animation.setKeyValueAt(0.5, shrink_geometry)
        animation.setKeyValueAt(1, original_geometry)
        
        animation.start()
    
    def load_sounds(self):
        if os.path.exists(self.sounds_dir):
            for file_name in os.listdir(self.sounds_dir):
                full_path = os.path.join(self.sounds_dir, file_name)
                if os.path.isfile(full_path):
                    self.add_sound_button(full_path)
                    
    def edit_sound_name(self, file_name, sound_button):
        new_name, ok = QFileDialog.getSaveFileName(self, "Rename Sound File", file_name, "Audio Files (*.wav *.mp3)")
        if ok and new_name:
            new_file_path = os.path.join(self.sounds_dir, os.path.basename(new_name))
            os.rename(file_name, new_file_path)
            sound_button.setText(os.path.basename(new_file_path))
            self.sounds.remove(file_name)
            self.sounds.append(new_file_path)

    def delete_sound(self, file_name, sound_button_layout):
        reply = QMessageBox.question(self, 'Delete Sound', f"Are you sure you want to delete {os.path.basename(file_name)}?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            os.remove(file_name)
            self.sounds.remove(file_name)
            self.clear_layout(sound_button_layout)

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SoundboardApp()
    sys.exit(app.exec_())
