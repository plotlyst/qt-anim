from qtpy.QtWidgets import QPushButton, QWidget, QHBoxLayout

from qtanim import fade_in, fade_out, shake, flash, glow, pulse


def test_fade(qtbot):
    widget = QWidget()
    widget.setLayout(QHBoxLayout())
    widget.layout().addWidget(QPushButton('btn1', widget))
    btn = QPushButton('Test button')
    widget.layout().addWidget(btn)
    qtbot.addWidget(widget)
    widget.show()

    fade_out(btn)
    qtbot.wait(300)
    assert btn.isHidden()
    fade_in(btn)
    qtbot.wait(250)
    assert btn.isVisible()


def test_shake(qtbot):
    btn = QPushButton('Test button')
    qtbot.addWidget(btn)
    btn.show()

    shake(btn)
    qtbot.wait(250)


def test_flash(qtbot):
    btn = QPushButton('Test button')
    qtbot.addWidget(btn)
    btn.show()

    flash(btn)
    qtbot.wait(250)


def test_glow(qtbot):
    btn = QPushButton('Test button')
    qtbot.addWidget(btn)
    btn.show()

    glow(btn)
    qtbot.wait(250)


def test_pulse(qtbot):
    btn = QPushButton('Test button')
    qtbot.addWidget(btn)
    btn.show()

    pulse(btn)
    qtbot.wait(250)
