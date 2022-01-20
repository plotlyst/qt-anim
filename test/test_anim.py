from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout

from qtanim import fade_in, fade_out


def test_flash(qtbot):
    widget = QWidget()
    widget.setLayout(QHBoxLayout())
    widget.layout().addWidget(QPushButton('btn1', widget))
    btn = QPushButton('Test button')
    widget.layout().addWidget(btn)
    qtbot.addWidget(widget)
    widget.show()

    # shake(btn)
    fade_out(btn)
    qtbot.wait(500)
    fade_in(btn)

    qtbot.stop()
