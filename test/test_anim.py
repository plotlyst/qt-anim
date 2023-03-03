from qtpy.QtWidgets import QPushButton, QWidget, QHBoxLayout

from qtanim import fade_in, fade_out, shake, glow, colorize
from qtanim.animations import pulse


def wait_for_finished(qtbot, anim, timeout: int = 3000):
    with qtbot.waitSignal(anim.finished, timeout=timeout):
        pass


def test_fade(qtbot):
    widget = QWidget()
    widget.setLayout(QHBoxLayout())
    widget.layout().addWidget(QPushButton('btn1', widget))
    btn = QPushButton('Test button')
    widget.layout().addWidget(btn)
    qtbot.addWidget(widget)
    widget.show()

    anim = fade_out(btn)
    wait_for_finished(qtbot, anim)
    assert btn.isHidden()

    anim = fade_in(btn)
    wait_for_finished(qtbot, anim)
    assert btn.isVisible()


def test_shake(qtbot):
    btn = QPushButton('Test button')
    qtbot.addWidget(btn)
    btn.show()

    anim = shake(btn)
    wait_for_finished(qtbot, anim, 10000)


# def test_flash(qtbot):
#     btn = QPushButton('Test button')
#     qtbot.addWidget(btn)
#     btn.show()
#
#     anim = flash(btn)
#     wait_for_finished(qtbot, anim)


def test_glow(qtbot):
    btn = QPushButton('Test button')
    qtbot.addWidget(btn)
    btn.show()

    anim = glow(btn)
    wait_for_finished(qtbot, anim)


def test_pulse(qtbot):
    btn = QPushButton('Test button')
    qtbot.addWidget(btn)
    btn.show()

    anim = pulse(btn)
    wait_for_finished(qtbot, anim)


def test_colorize(qtbot):
    btn = QPushButton('Test button')
    qtbot.addWidget(btn)
    btn.show()

    anim = colorize(btn)
    wait_for_finished(qtbot, anim)
