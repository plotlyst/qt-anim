import sys

import qtawesome
from qtpy.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QVBoxLayout

import qtanim


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        self.widget.setLayout(QVBoxLayout())

        self.btnFlash = QPushButton('Flash')
        self.btnFlash.setIcon(qtawesome.icon('fa5s.cog'))
        self.btnShake = QPushButton('Shake')
        self.btnFadeIn = QPushButton('Fade in')
        self.btnFadeOut = QPushButton('Fade out')
        self.btnPlay = QPushButton('Play all')
        self.btnGlow = QPushButton('Glow')
        self.btnColorize = QPushButton('Colorize')
        self.btnColorize.setIcon(qtawesome.icon('fa5s.cog'))
        self.btnPulse = QPushButton('Pulse')

        font = self.btnPlay.font()
        font.setBold(True)
        self.btnPlay.setFont(font)
        self.btnRevert = QPushButton('Revert')

        self.widget.layout().addWidget(self.btnFlash)
        self.widget.layout().addWidget(self.btnShake)
        self.widget.layout().addWidget(self.btnFadeIn)
        self.widget.layout().addWidget(self.btnFadeOut)
        self.widget.layout().addWidget(self.btnGlow)
        self.widget.layout().addWidget(self.btnColorize)
        self.widget.layout().addWidget(self.btnPulse)

        self.widget.layout().addWidget(self.btnPlay)
        self.widget.layout().addWidget(self.btnRevert)

        self.btnFlash.clicked.connect(lambda: qtanim.flash(self.btnFlash))
        self.btnShake.clicked.connect(lambda: qtanim.shake(self.btnShake))
        self.btnFadeIn.clicked.connect(lambda: qtanim.fade_in(self.btnFadeIn))
        self.btnFadeOut.clicked.connect(lambda: qtanim.fade_out(self.btnFadeOut))
        self.btnGlow.clicked.connect(lambda: qtanim.glow(self.btnGlow))
        self.btnColorize.clicked.connect(lambda: qtanim.colorize(self.btnColorize, duration=1000, strength=0.8))
        self.btnPulse.clicked.connect(lambda: qtanim.pulse(self.btnPulse))

        self.btnPlay.clicked.connect(self._play)
        self.btnRevert.clicked.connect(lambda: qtanim.fade_in(self.btnFadeOut))

    def _play(self):
        self.btnFlash.click()
        self.btnShake.click()
        self.btnFadeIn.click()
        self.btnFadeOut.click()
        self.btnGlow.click()
        self.btnColorize.click()
        self.btnPulse.click()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    app.exec()
