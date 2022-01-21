import sys

from qtpy.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QVBoxLayout

import qtanim


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        self.widget.setLayout(QVBoxLayout())

        self.btnFlash = QPushButton('Flash')
        self.btnShake = QPushButton('Shake')
        self.btnFadeIn = QPushButton('Fade in')
        self.btnFadeOut = QPushButton('Fade out')
        self.btnPlay = QPushButton('Play all')
        font = self.btnPlay.font()
        font.setBold(True)
        self.btnPlay.setFont(font)
        self.btnRevert = QPushButton('Revert')

        self.widget.layout().addWidget(self.btnFlash)
        self.widget.layout().addWidget(self.btnShake)
        self.widget.layout().addWidget(self.btnFadeIn)
        self.widget.layout().addWidget(self.btnFadeOut)
        self.widget.layout().addWidget(self.btnPlay)
        self.widget.layout().addWidget(self.btnRevert)

        self.btnFlash.clicked.connect(lambda: qtanim.flash(self.btnFlash))
        self.btnShake.clicked.connect(lambda: qtanim.shake(self.btnShake))
        self.btnFadeIn.clicked.connect(lambda: qtanim.fade_in(self.btnFadeIn))
        self.btnFadeOut.clicked.connect(lambda: qtanim.fade_out(self.btnFadeOut))
        self.btnPlay.clicked.connect(self._play)
        self.btnRevert.clicked.connect(lambda: qtanim.fade_in(self.btnFadeOut))

    def _play(self):
        self.btnFlash.click()
        self.btnShake.click()
        self.btnFadeIn.click()
        self.btnFadeOut.click()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.move(QApplication.desktop().screen().rect().center())
    window.show()

    app.exec()
