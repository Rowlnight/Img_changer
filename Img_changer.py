import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QMovie
from PyQt5 import QtGui, QtWidgets
import os, random, time
import numpy as np
import mutagen
from mutagen.id3 import APIC, ID3
from mutagen.aiff import AIFF
from mutagen.easyid3 import EasyID3


class Img_changer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initialize_dependencies()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(750, 610)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit_music = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_music.setEnabled(False)
        self.lineEdit_music.setGeometry(QtCore.QRect(10, 400, 561, 20))
        self.lineEdit_music.setObjectName("lineEdit_music")
        self.lineEdit_img = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_img.setEnabled(False)
        self.lineEdit_img.setGeometry(QtCore.QRect(10, 430, 561, 21))
        self.lineEdit_img.setObjectName("lineEdit_img")
        self.main_console = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.main_console.setEnabled(True)
        self.main_console.setGeometry(QtCore.QRect(10, 10, 731, 311))
        self.main_console.setObjectName("main_console")
        self.choice_music_btn = QtWidgets.QPushButton(self.centralwidget)
        self.choice_music_btn.setGeometry(QtCore.QRect(570, 400, 171, 21))
        self.choice_music_btn.setObjectName("choice_music_btn")
        self.choice_img_btn = QtWidgets.QPushButton(self.centralwidget)
        self.choice_img_btn.setGeometry(QtCore.QRect(570, 430, 171, 21))
        self.choice_img_btn.setObjectName("choice_img_btn")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 330, 731, 21))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(10, 540, 731, 41))
        self.start_btn.setObjectName("start_btn")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setGeometry(QtCore.QRect(150, 470, 591, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(10, 470, 131, 21))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 500, 171, 17))
        self.checkBox_2.setObjectName("checkBox_2")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 380, 751, 16))
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 370, 741, 16))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 761, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.choice_music_btn.setText(_translate("MainWindow", "Выбрать папку с музыкой"))
        self.choice_img_btn.setText(_translate("MainWindow", "Выбрать папку с картинками"))
        self.start_btn.setText(_translate("MainWindow", "Начать!"))
        self.checkBox.setText(_translate("MainWindow", "Изменить альбом"))
        self.checkBox_2.setText(_translate("MainWindow", "Пронумеровать треки"))
        self.label.setText(_translate("MainWindow", "Настройка запуска"))

    def initialize_dependencies(self):
        self.choice_music_btn.clicked.connect(self.choice_music)
        self.choice_img_btn.clicked.connect(self.choice_img)
        self.start_btn.clicked.connect(self.start_main_func)
        self.progressBar.setValue(0)
        self.main_console.setWordWrapMode(self.main_console.wordWrapMode())
        self.main_console.setReadOnly(True)
        self.checkBox.stateChanged.connect(self.show_albom_line)

    def show_albom_line(self):
        if self.checkBox.isChecked():
            self.lineEdit.setEnabled(True)
        else:
            self.lineEdit.clear()
            self.lineEdit.setEnabled(False)

    def choice_music(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Select a Dir", ".")
        self.lineEdit_music.setText(dirlist)

    def choice_img(self):
        dirlist = QFileDialog.getExistingDirectory(self, "Select a Dir", ".")
        self.lineEdit_img.setText(dirlist)

    def start_main_func(self):
        try:
            self.main_console.clear()
            self.thread = Main_thread(self.lineEdit_music.text(),
                                      self.lineEdit_img.text(),
                                      self.checkBox.isChecked(),
                                      self.lineEdit.text(),
                                      self.checkBox_2.isChecked()
                                      )
            
            self.thread.signal.connect(self.graphics_update)
            self.thread.start()
        except Exception as error:
            print(error)

    def graphics_update(self, data):
        tipe = data[0]
        value = data[1]
        if tipe == 'message':
            self.main_console.appendPlainText(value)
        elif tipe == 'set_max':
            self.progressBar.setMaximum(value)
        elif tipe == 'set_value':
            self.progressBar.setValue(value)

                     
class Main_thread(QtCore.QThread):
    signal = QtCore.pyqtSignal(list)

    def __init__(self, music_dir, img_dir, change_albom, albom, enumerate_files):
        super().__init__()
        self.music_dir = music_dir
        self.img_dir = img_dir
        self.change_albom = change_albom
        self.albom = albom
        self.enumerate_files = enumerate_files

    def run(self):
        if self.music_dir == '' or self.img_dir == '':
            self.signal.emit(['message', 'Не все поля заполнены!'])
        else:
            progress = 0
            counter_files = 0
            counter_alboms = 0
            counter_covers = 0
            counter_enumerate = 0
            troble_list = []
            troble_covers_list = []
            all_files_list = os.listdir(self.music_dir)
            all_img_list = os.listdir(self.img_dir)
            self.signal.emit(['set_max', len(all_files_list)])

            files_list = []
            img_list = []

            for file in all_files_list:
                if '.mp3' in file:
                    files_list.append(file)

            for file in all_img_list:
                if '.png' in file or '.jpg' in file or '.jpeg' in file:
                    img_list.append(file)

            if img_list == [] or files_list == []:
                self.signal.emit(['message', f'В одной из указанных папок отсутствуют необходимые файлы!'])
                return

            self.signal.emit(['set_max', len(files_list)])

            self.signal.emit(['message', f'Файлов MP3 - {len(files_list)}'])
            self.signal.emit(['message', f'Картинок - {len(img_list)}'])

            if len(files_list) <= len(img_list):
                self.signal.emit(['message', f'Режим распределения - рандомное_распределение_без_повторов'])
            elif len(files_list) > len(img_list):
                self.signal.emit(['message', f'Режим распределения - рандомное_распределение_с_повторами'])

            self.signal.emit(['set_value', 0])
            time.sleep(3)

            for mp3_file in files_list:
                successful = False
                counter = 0
                try:
                    if img_list != []:
                        img = random.choice(img_list)
                        img_list.remove(img)
                    else:
                        for file in all_img_list:
                            if '.png' in file or '.jpg' in file or '.jpeg' in file:
                                img_list.append(file)
                        img = random.choice(img_list)
                        img_list.remove(img)

                    new_img = open(self.img_dir + '/' + img, 'rb')
                    track = self.music_dir + '/' + mp3_file
                except Exception as error:
                    print(error)
                
                try:
                    try:
                        file = ID3(track)
                        file.delall("APIC")
                        file.save()
                        with new_img as albumart:
                            if '.png' in img:
                                file.add(APIC(encoding=3, mime='image/png', type=3, desc=u'Cover', data=albumart.read()))
                            elif '.jpg' in img or '.jpeg' in img:
                                file.add(APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=albumart.read()))
                        file.save(v1=0,v2_version=3)
                        self.signal.emit(['message', f'Обложка файла {mp3_file} изменена на {img}'])
                        counter_covers = counter_covers + 1

                        if self.change_albom:
                            tags = EasyID3(track)
                            tags['album'] = self.albom
                            tags.save(v1=0,v2_version=3)
                            self.signal.emit(['message', f'Альбом файла {mp3_file} изменён на {self.albom}'])
                            counter_alboms = counter_alboms + 1

                        if self.enumerate_files:
                            tags = EasyID3(track)
                            tags['tracknumber'] = str(counter_files + 1)
                            tags.save(v1=0,v2_version=3)
                            self.signal.emit(['message', f'Файл {mp3_file} получает номер - {str(counter_files + 1)}'])
                            counter_enumerate = counter_enumerate + 1
                                    
                    except Exception as error:
                        troble_covers_list.append(mp3_file)
                        file = mutagen.File(track, easy=True)
                        file.add_tags()
                        print(error)

                        self.signal.emit(['message', f'Не удалось изменить обложку файла {mp3_file}'])

                        if self.change_albom:
                            file['album'] = self.albom
                            file.save(v1=0,v2_version=3)
                            self.signal.emit(['message', f'Альбом файла {mp3_file} изменён на {self.albom}'])
                            counter_alboms = counter_alboms + 1

                        if self.enumerate_files:
                            file['tracknumber'] = str(counter_files + 1)
                            file.save(v1=0,v2_version=3)
                            self.signal.emit(['message', f'Файл {mp3_file} получает номер - {str(counter_files + 1)}'])
                            counter_enumerate = counter_enumerate + 1

                    progress = progress + 1
                    self.signal.emit(['set_value', progress])
                    successful = True
                    counter_files = counter_files + 1
                except Exception as error:
                    counter = counter + 1
                    self.signal.emit(['message', f'Не удалось отредактировать файл {mp3_file}'])
                    troble_list.append(mp3_file)
                    progress = progress + 1
                    self.signal.emit(['set_value', progress])

            self.signal.emit(['message', f'\n ---> Программа завершила работу:\n'])
            self.signal.emit(['message', f' ----->     изменена обложка в {counter_covers} из {len(files_list)} файлов'])
            self.signal.emit(['message', f' ----->     изменён альбом в {counter_alboms} из {len(files_list)} файлов'])
            self.signal.emit(['message', f' ----->     изменён номер в {counter_enumerate} из {len(files_list)} файлов\n'])
            if troble_covers_list != []:
                self.signal.emit(['message', f'---> Не удалось сменить обложку у файлов {troble_covers_list}\n'])
            if troble_list != []:
                self.signal.emit(['message', f'---> Скорее всего файлы {troble_list} запрещены для редактирования или повреждены!'])


dir = os.path.abspath(os.curdir)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    file = QtCore.QFile(f"dark_theme.qss")
    file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
    stream = QtCore.QTextStream(file)
    app.setStyleSheet(stream.readAll())
    ex = Img_changer()
    ex.show()
    sys.exit(app.exec_())
