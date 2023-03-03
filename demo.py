import sys

import qtawesome
from PyQt5.QtWidgets import QToolButton, QLabel, QFrame
from qthandy import line, vbox
from qtpy.QtCore import QPropertyAnimation
from qtpy.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QVBoxLayout

import qtanim
from qtanim import prop_anim_config


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        self.widget.setLayout(QVBoxLayout())

        prop_anim_config.deletion_policy = QPropertyAnimation.DeletionPolicy.DeleteWhenStopped

        # self.btnFlash = QPushButton('Flash')
        # self.btnFlash.setIcon(qtawesome.icon('fa5s.cog'))
        self.btnShake = QPushButton('Shake')
        self.btnFadeIn = QPushButton('Fade in')
        self.btnFadeOut = QPushButton('Fade out')
        self.btnPlay = QPushButton('Play all')
        self.btnGlow = QPushButton('Glow')
        self.btnColorize = QPushButton('Colorize')
        self.btnColorize.setIcon(qtawesome.icon('fa5s.cog'))
        self.btnPulse = QPushButton('Pulse')
        self.btnToggle = QToolButton()
        self.btnToggle.setCheckable(True)
        self.wdgBar = QFrame()
        self.wdgBar.setStyleSheet('.QFrame{ border: 1px solid black;}')
        vbox(self.wdgBar)
        self.wdgBar.layout().addWidget(QLabel('Menu 1'))
        self.wdgBar.layout().addWidget(QLabel('Menu 2'))

        font = self.btnPlay.font()
        font.setBold(True)
        self.btnPlay.setFont(font)
        self.btnRevert = QPushButton('Revert')

        # self.widget.layout().addWidget(self.btnFlash)
        self.widget.layout().addWidget(self.btnShake)
        self.widget.layout().addWidget(self.btnFadeIn)
        self.widget.layout().addWidget(self.btnFadeOut)
        self.widget.layout().addWidget(self.btnGlow)
        self.widget.layout().addWidget(self.btnColorize)
        self.widget.layout().addWidget(self.btnPulse)
        self.widget.layout().addWidget(self.btnToggle)
        self.widget.layout().addWidget(self.wdgBar)
        self.wdgBar.setHidden(True)

        self.widget.layout().addWidget(line())

        self.widget.layout().addWidget(self.btnPlay)
        self.widget.layout().addWidget(self.btnRevert)

        # self.btnFlash.clicked.connect(lambda: qtanim.flash(self.btnFlash))
        self.btnShake.clicked.connect(lambda: qtanim.shake(self.btnShake))
        self.btnFadeIn.clicked.connect(lambda: qtanim.fade_in(self.btnFadeIn))
        self.btnFadeOut.clicked.connect(lambda: qtanim.fade_out(self.btnFadeOut))
        self.btnGlow.clicked.connect(lambda: qtanim.glow(self.btnGlow))
        self.btnColorize.clicked.connect(lambda: qtanim.colorize(self.btnColorize, duration=1000, strength=0.8))
        self.btnPulse.clicked.connect(lambda: qtanim.animations.pulse(self.btnPulse))
        self.btnToggle.toggled.connect(self.toggleMenu)

        self.btnPlay.clicked.connect(self._play)
        self.btnRevert.clicked.connect(lambda: qtanim.fade_in(self.btnFadeOut))

    def toggleMenu(self, checked: bool):
        qtanim.toggle_expansion(self.wdgBar, checked)

    def _play(self):
        # self.btnFlash.click()
        self.btnShake.click()
        self.btnFadeIn.click()
        self.btnFadeOut.click()
        self.btnGlow.click()
        self.btnColorize.click()
        self.btnPulse.click()
        self.btnToggle.toggle()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    app.exec()
