import os
os.system('cls')

import json
import tempfile

from translate import Translator
import speech_recognition as sr
from gtts import gTTS
import pygame

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox, QTextEdit,QCheckBox
)
from PyQt5.QtCore import Qt


app = QApplication([])


style_title = """
    font-size: 30px;
    color: #0cb310;
    border: 2px solid #50856e;
    background-color: #b6d6b7;
"""

style_combo = """
    font-size: 22px;
    color:#f5d151;
    background-color: #a6b089;
    border: 2px solid #2f4a19;
"""

style_direct_label = """
    font-size: 15px;
    color:#8c7527;
    background-color: #f2d574;
    border: 2px solid #2f4a19;
    padding: 10px 80px;
"""

style_label_second = """
    font-size: 25px;
    color:#8c7527;
    background-color: #f2d574;
    border: 2px solid #2f4a19;
    padding: 10px;
"""

style_input = """
    font-size: 22px;
    border: 2px solid #066908;
    color: #474747;
    background-color: #a4edcd;
"""

style_btn = """
    font-size: 22px;
    border: 3px solid #066908;
    border-radius: 15px;
    color: #f5d151;
    background-color: #7594ba;
    padding: 10px;
"""

style_close_btn = """
    font-size: 22px;
    border: 3px solid #066908;
    border-radius: 15px;
    background-color: #f72a45;
    padding: 10px;
"""

style_checkbox = """
    font-size: 20px;
    font-weight: bold;
    color:#f5d151;
"""


Languages = {
    "O'zbek": "uz",
    "English": "en",
    "Russian": "ru",
    "Turk": "tr",
    "Arab": "ar",
    "Koreys":"ko",
    "Tojik": "tg",
    "Qozoq": "kk"
}

# ========== Nutqni aniqlash uchun tillar ==========

SpeechLanguages = {
    "O'zbek": "uz-UZ",
    "English": "en-US",
    "Russian": "ru-RU",
    "Turk": "tr-TR",
    "Arab": "ar-AR",
    "Koreys":"ko-KO",
    "Tojik": "tg-TG",
    "Qozoq": "kk-KK"
}

with open ('short_gaps.json') as file:
    keys = []
    data = json.load(file)
    # print(data)
    for a in data:
        k = a.keys()
        keys.extend(k)
    
    # print(keys)
    
#================================  SECOND WINDOW  ==============================================>

class SecondWindow(QWidget):
    """Qisqa va Common ishlatiladigan qisqa gaplar qoshish."""
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Asosiy oynaga havola (reference)
        self.setWindowTitle("Short and Common Sentences")
        self.resize(600, 400)
        
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        
        self.label_second = QLabel()
        self.label_second.setText("Expending with Short and Common Sentences:")
        self.label_second.setStyleSheet(style_label_second)
        self.vbox.addWidget(self.label_second)
        
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('The number of characters should be more than 5.')
        self.text_edit.setStyleSheet(style_input)
        self.vbox.addWidget(self.text_edit)
        
        
        self.back_btn = QPushButton("⬅ Back to Main Window")
        self.back_btn.setStyleSheet("font-size: 14px; padding: 8px; background-color: #34495e; color: white; font-weight: bold;")
        self.back_btn.clicked.connect(self.back_to_main)
        self.hbox.addWidget(self.back_btn)
        
        
        self.add_btn = QPushButton("Add Combo and Close Window!")
        self.add_btn.setStyleSheet("font-size: 14px; padding: 8px; background-color: #34495e; color: #f72a45 ; font-weight: bold;")
        self.add_btn.clicked.connect(self.add_short)
        self.hbox.addWidget(self.add_btn)
        
        
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)
        
    def add_short(self):
        text =self.text_edit.toPlainText()
        if len(text) > 5 and text not in keys and text != "Incorrect input...":
             
            new = {}
            with open ('short_gaps.json') as file1:
                data = json.load(file1)
                new[text] = text
                data.append(new)
                
            with open ('short_gaps.json','w') as file2:
                json.dump(data,file2, indent=4, ensure_ascii=False)
                    
            self.text_edit.setText("Malumot saqlandi. Interfeysga qayta kiring!")
            # self.main_window.show() 
            self.close()
        else:
            self.text_edit.setText("Incorrect input...")


    def back_to_main(self):
        """Asosiy oynani ko'rsatish va joriy oynani yopish"""
        self.main_window.show()  # Asosiy oynani qayta ochish (barcha ma'lumotlari saqlangan holda)
        self.close()
        
        
# =========================  Main Window  ================================

class TarjimonApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Voice Translator")
        self.setStyleSheet('background-color: #19385e;')
        self.resize(500, 800)

        self.vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()


        self.sarlavha = QLabel("Welcome to Translator")
        self.sarlavha.setFixedHeight(60)
        self.sarlavha.setStyleSheet(style_title)
        self.sarlavha.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.sarlavha)


        self._from_lang = QComboBox()
        self._from_lang.addItems(Languages.keys())
        self._from_lang.setStyleSheet(style_combo)
        self.hbox1.addWidget(self._from_lang)
        
        
        self.direct_label = QLabel("<== From | To ==>")
        self.direct_label.setStyleSheet(style_direct_label)
        self.hbox1.addWidget(self.direct_label)
        
        
        self._to_lang = QComboBox()
        self._to_lang.addItems(Languages.keys())
        self._to_lang.setStyleSheet(style_combo)
        self.hbox1.addWidget(self._to_lang)
        
        self.vbox.addLayout(self.hbox1)           # ===== From <==> To combo boxes =====


        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText(
            "Type text or speak into the microphone..."
        )
        self.input_area.setStyleSheet(style_input)
        self.input_area.setFixedHeight(150)
        self.vbox.addWidget(self.input_area)


        self.mic_btn = QPushButton("🎤 Input by Voice")
        self.mic_btn.setStyleSheet(style_btn)
        self.mic_btn.clicked.connect(self.ozvodan_matn)
        self.hbox3.addWidget(self.mic_btn)
        

        self.short_gaps = QComboBox()
        self.short_gaps.addItems(keys)
        self.short_gaps.setStyleSheet(style_combo)
        self.short_gaps.currentTextChanged.connect(self.input_area.setText)
        self.hbox3.addWidget(self.short_gaps)
        

        self.checkbox = QCheckBox("During typing TR")
        self.checkbox.stateChanged.connect(self.checkbox_textedit)
        self.checkbox.setStyleSheet(style_checkbox)
        self.hbox3.addWidget(self.checkbox)
        
        
        
        self.btn_shorts = QPushButton("Add Short Combo")
        self.btn_shorts.setStyleSheet(style_btn)
        self.btn_shorts.clicked.connect(self.open_second_window)  
        self.hbox3.addWidget(self.btn_shorts)
        
        self.vbox.addLayout(self.hbox3)
        

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setPlaceholderText("Please Wait, Translating...")
        self.result_area.setStyleSheet(style_input)
        self.result_area.setFixedHeight(150)
        self.vbox.addWidget(self.result_area)


        self.speak_btn = QPushButton("🔊 Hearing the result...")
        self.speak_btn.setStyleSheet(style_btn)
        self.speak_btn.clicked.connect(self.ovozi_chiqarish)
        self.hbox2.addWidget(self.speak_btn)


        self.close_btn = QPushButton("Close all Window!")
        self.close_btn.setStyleSheet(style_close_btn)
        self.close_btn.clicked.connect(self.close_win)
        self.hbox2.addWidget(self.close_btn)
        self.vbox.addLayout(self.hbox2) 
        
               
        self.tarjima_btn = QPushButton("Translate")
        self.tarjima_btn.setStyleSheet(style_btn)
        self.tarjima_btn.clicked.connect(self.tarjima_qilish)
        self.hbox2.addWidget(self.tarjima_btn)


        self.setLayout(self.vbox)
        self.show()
        
        
    def checkbox_textedit(self):
        if self.checkbox.isChecked():
            self.input_area.textChanged.connect(self.tarjima_qilish)
        
        
    def open_second_window(self):
        """Short and Common Sentences"""
        if not keys:
            QMessageBox.warning(self, "Ogohlantirish", "Ma'lumotlar yuklanmagan!")
            return
            
        self.second_window = SecondWindow(self)
        self.second_window.show()
        self.hide()


    def close_win(self):
        self.close()

# =========================== Ovozni Matnga va Matnni Ovozga aylantirish jarayoni. ====================================
    # 1. Ovozdan matn olish
    def ozvodan_matn(self):
        recognizer = sr.Recognizer()

        try:
            self.mic_btn.setEnabled(False)
            self.mic_btn.setText("Tinglanmoqda...")

            with sr.Microphone() as source:
                QMessageBox.information(
                    self,
                    "Mikrofon",
                    "OK tugmasini bosing va gapiring."
                )

                recognizer.adjust_for_ambient_noise(
                    source, duration=0.5
                )

                audio = recognizer.listen(
                    source, timeout=5, phrase_time_limit=15
                )

            til_nomi = self._from_lang.currentText()
            til_kodi = SpeechLanguages[til_nomi]

            matn = recognizer.recognize_google(
                audio, language=til_kodi
            )

            # Aniqlangan matnni kiritish maydoniga yozish
            self.input_area.setPlainText(matn)

        except sr.WaitTimeoutError:
            QMessageBox.warning(
                self, "Ogohlantirish",
                "Ovoz aniqlanmadi. Qayta urinib ko'ring."
            )

        except sr.UnknownValueError:
            QMessageBox.warning(
                self, "Ogohlantirish",
                "Gapingizni tushunib bo'lmadi. Aniqroq gapiring."
            )

        except sr.RequestError as e:
            QMessageBox.critical(
                self, "Internet xatosi",
                f"Ovozni aniqlash xizmatida xato:\n{e}"
            )

        except Exception as e:
            QMessageBox.critical(
                self, "Xatolik",
                f"Mikrofonni tekshiring:\n{e}"
            )

        finally:
            self.mic_btn.setEnabled(True)
            self.mic_btn.setText("🎤 Ovoz orqali kiritish")

    # 2. Matnni tarjima qilish
    def tarjima_qilish(self):
        matn = self.input_area.toPlainText().strip()

        if not matn:
            QMessageBox.warning(
                self, "Ogohlantirish",
                "Avval matn kiriting yoki gapiring."
            )
            return

        from_name = self._from_lang.currentText()
        to_name = self._to_lang.currentText()

        from_code = Languages[from_name]
        to_code = Languages[to_name]

        if from_code == to_code:
            self.result_area.setPlainText(matn)
            return

        try:
            tarjimon = Translator(
                from_lang=from_code,
                to_lang=to_code
            )

            natija = tarjimon.translate(matn)
            self.result_area.setPlainText(natija)

        except Exception as e:
            QMessageBox.critical(
                self, "Tarjima xatosi",
                f"Tarjima bajarilmadi:\n{e}"
            )

    # 3. Tarjimani ovoz chiqarib o'qish
    def ovozi_chiqarish(self):
        matn = self.result_area.toPlainText().strip()

        if not matn:
            QMessageBox.warning(
                self, "Ogohlantirish",
                "Avval matnni tarjima qiling."
            )
            return

        til_nomi = self._to_lang.currentText()
        til_kodi = Languages[til_nomi]

        try:
            # Matndan ovoz yaratish
            ovoz = gTTS(text=matn, lang=til_kodi)

            # Vaqtinchalik MP3 fayl yaratish
            with tempfile.NamedTemporaryFile(
                suffix=".mp3", delete=False
            ) as fayl:
                fayl_nomi = fayl.name

            ovoz.save(fayl_nomi)

            # Ovoz ijrosi
            pygame.mixer.init()
            pygame.mixer.music.load(fayl_nomi)
            pygame.mixer.music.play()

            QMessageBox.information(
                self, "Ovoz",
                "Tarjima ovozli tarzda ijro etilmoqda."
            )

        except Exception as e:
            QMessageBox.critical(
                self, "Ovoz xatosi",
                f"Ovozni chiqarib bo'lmadi:\n{e}"
            )
# =========================================  Ovoz bilan boladigan jarayon tugallandi. ================================

window = TarjimonApp()
app.exec_()