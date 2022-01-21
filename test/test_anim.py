from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout

from qtanim import fade_in, fade_out, shake, flash


def test_fade(qtbot):
    widget = QWidget()
    widget.setLayout(QHBoxLayout())
    widget.layout().addWidget(QPushButton('btn1', widget))
    btn = QPushButton('Test button')
    widget.layout().addWidget(btn)
    qtbot.addWidget(widget)
    widget.show()

    fade_out(btn)
    fade_in(btn)


def test_shake(qtbot):
    btn = QPushButton('Test button')
    qtbot.addWidget(btn)
    btn.show()

    shake(btn)


def test_flash(qtbot):
    btn = QPushButton('Test button')
    qtbot.addWidget(btn)
    btn.show()

    flash(btn)
