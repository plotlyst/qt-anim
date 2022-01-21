from qtpy.QtCore import QPropertyAnimation
from qtpy.QtCore import Qt, QRect, QSequentialAnimationGroup, QEasingCurve
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QGraphicsColorizeEffect, QGraphicsOpacityEffect
from qtpy.QtWidgets import QWidget


def flash(widget: QWidget) -> QPropertyAnimation:
    effect = QGraphicsColorizeEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b'color', widget)
    animation.setLoopCount(5)
    animation.setDuration(250)
    animation.setStartValue(QColor(Qt.GlobalColor.blue))
    animation.setEndValue(QColor(Qt.GlobalColor.red))
    animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    return animation


def shake(widget: QWidget, distance: int = 5, loop: int = 3) -> QSequentialAnimationGroup:
    original = widget.geometry()
    left_geo: QRect = widget.geometry()
    left_geo.setX(left_geo.x() - distance)
    right_geo: QRect = widget.geometry()
    right_geo.setX(right_geo.x() + distance)

    first_animation = QPropertyAnimation(widget, b'geometry', widget)
    first_animation.setDuration(20)
    first_animation.setStartValue(original)
    first_animation.setEndValue(left_geo)

    shake_animation = QPropertyAnimation(widget, b'geometry', widget)
    shake_animation.setDuration(100)
    shake_animation.setStartValue(left_geo)
    shake_animation.setEndValue(right_geo)
    shake_animation.setLoopCount(loop)

    end_animation = QPropertyAnimation(widget, b'geometry', widget)
    end_animation.setDuration(20)
    end_animation.setStartValue(right_geo)
    end_animation.setEndValue(widget.geometry())

    sequence = QSequentialAnimationGroup(widget)
    sequence.addAnimation(first_animation)
    sequence.addAnimation(shake_animation)
    sequence.addAnimation(end_animation)

    sequence.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    return sequence


def fade_in(widget: QWidget, duration: int = 250) -> QPropertyAnimation:
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b'opacity', widget)
    animation.setDuration(duration)
    animation.setStartValue(0)
    animation.setEndValue(1)
    animation.setEasingCurve(QEasingCurve.Type.InBack)
    widget.setVisible(True)
    animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    return animation


def fade_out(widget: QWidget, duration: int = 250) -> QPropertyAnimation:
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b'opacity', widget)
    animation.setDuration(duration)
    animation.setStartValue(1)
    animation.setEndValue(0)
    animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
    animation.finished.connect(lambda: widget.setHidden(True))

    return animation
