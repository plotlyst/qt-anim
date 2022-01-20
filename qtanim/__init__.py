from qtpy.QtCore import QPropertyAnimation
from qtpy.QtCore import Qt, QRect, QSequentialAnimationGroup, QEasingCurve
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QGraphicsColorizeEffect, QGraphicsOpacityEffect
from qtpy.QtWidgets import QWidget


def flash(widget: QWidget):
    effect = QGraphicsColorizeEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b'color', widget)
    animation.setLoopCount(5)
    animation.setDuration(250)
    animation.setStartValue(QColor(Qt.GlobalColor.blue))
    animation.setEndValue(QColor(Qt.GlobalColor.red))
    animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)


def shake(widget: QWidget, distance: int = 5, loop: int = 3):
    original = widget.geometry()

    first_animation = QPropertyAnimation(widget, b'geometry', widget)
    first_animation.setStartValue(original)
    left_geo: QRect = widget.geometry()
    left_geo.setX(left_geo.x() - distance)
    right_geo: QRect = widget.geometry()
    right_geo.setX(left_geo.x() + distance)

    first_animation.setEndValue(left_geo)

    shake_animation = QPropertyAnimation(widget, b'geometry', widget)
    shake_animation.setStartValue(left_geo)
    shake_animation.setEndValue(right_geo)
    shake_animation.setLoopCount(loop)

    end_animation = QPropertyAnimation(widget, b'geometry', widget)
    end_animation.setStartValue(left_geo)
    end_animation.setEndValue(widget.geometry())

    sequence = QSequentialAnimationGroup(widget)
    sequence.addAnimation(first_animation)
    sequence.addAnimation(shake_animation)
    sequence.addAnimation(end_animation)

    sequence.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)


def fade_in(widget: QWidget, duration: int = 350):
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b'opacity', widget)
    animation.setDuration(duration)
    animation.setStartValue(0)
    animation.setEndValue(1)
    animation.setEasingCurve(QEasingCurve.Type.InBack)
    widget.setVisible(True)
    animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)


def fade_out(widget: QWidget, duration: int = 350):
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b'opacity', widget)
    animation.setDuration(duration)
    animation.setStartValue(1)
    animation.setEndValue(0)
    animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
    animation.finished.connect(lambda: widget.setHidden(True))
