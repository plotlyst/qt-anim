from dataclasses import dataclass
from typing import Optional

from qtpy.QtCore import QPropertyAnimation, QObject
from qtpy.QtCore import Qt, QRect, QSequentialAnimationGroup, QEasingCurve, QParallelAnimationGroup, \
    QAbstractAnimation, QVariantAnimation
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QGraphicsColorizeEffect, QGraphicsOpacityEffect, QGraphicsDropShadowEffect
from qtpy.QtWidgets import QGraphicsObject, QWidget

from qtanim.util import reverse


@dataclass
class PropertyAnimationConfig:
    deletion_policy = QPropertyAnimation.DeletionPolicy.KeepWhenStopped


prop_anim_config = PropertyAnimationConfig()


# def flash(widget, start_color=QColor(Qt.blue), end_color: QColor = QColor(Qt.red), deletion=None) -> QAbstractAnimation:
#     effect = QGraphicsColorizeEffect(widget)
#     widget.setGraphicsEffect(effect)
#
#     animation = QPropertyAnimation(effect, b'color', widget)
#     animation.setLoopCount(5)
#     animation.setDuration(250)
#     animation.setStartValue(start_color)
#     animation.setEndValue(end_color)
#
#     _start(animation, deletion)
#     animation.finished.connect(lambda: widget.setGraphicsEffect(None))
#
#     return animation


def shake(widget, distance: int = 5, loop: int = 3, deletion=None, teardown=None) -> QAbstractAnimation:
    original = widget.geometry()
    left_geo: QRect = widget.geometry()
    left_geo.setX(left_geo.x() - distance)
    right_geo: QRect = widget.geometry()
    right_geo.setX(right_geo.x() + distance)

    first_animation = QPropertyAnimation(widget, b'geometry')
    __set_parent_if_qobj(first_animation, widget)
    first_animation.setDuration(20)
    first_animation.setStartValue(original)
    first_animation.setEndValue(left_geo)

    shake_animation = QPropertyAnimation(widget, b'geometry')
    __set_parent_if_qobj(shake_animation, widget)
    shake_animation.setDuration(100)
    shake_animation.setStartValue(left_geo)
    shake_animation.setEndValue(right_geo)
    shake_animation.setLoopCount(loop)

    end_animation = QPropertyAnimation(widget, b'geometry')
    __set_parent_if_qobj(end_animation, widget)
    end_animation.setDuration(20)
    end_animation.setStartValue(right_geo)
    end_animation.setEndValue(widget.geometry())

    sequence = QSequentialAnimationGroup()
    __set_parent_if_qobj(sequence, widget)
    sequence.addAnimation(first_animation)
    sequence.addAnimation(shake_animation)
    sequence.addAnimation(end_animation)

    _start(sequence, deletion, teardown)

    return sequence


def toggle_expansion(widget: QWidget, toggle: bool, duration: int = 250, deletion=None,
                     teardown=None) -> QAbstractAnimation:
    def reset(hidden: bool, defaultSize: Optional[int] = None):
        if hidden:
            widget.setHidden(True)
        if defaultSize is not None:
            widget.setMaximumWidth(defaultSize)

    def changed(value: int):
        widget.setMaximumWidth(value)

    animation = QVariantAnimation(widget)
    __set_parent_if_qobj(animation, widget)
    animation.setDuration(duration)

    defaultMaxWidth = widget.maximumWidth()

    if toggle:
        widget.setEnabled(True)
        widget.setMaximumWidth(1)
        widget.setVisible(True)

        animation.setEasingCurve(QEasingCurve.Type.InQuint)
        animation.setStartValue(1)
        if defaultMaxWidth:
            animation.setEndValue(min([defaultMaxWidth, widget.sizeHint().width()]))
        else:
            animation.setEndValue(widget.sizeHint().width())
        animation.finished.connect(lambda: reset(hidden=False, defaultSize=defaultMaxWidth))
    else:
        widget.setDisabled(True)

        animation.setEasingCurve(QEasingCurve.Type.InOutQuint)
        animation.setStartValue(widget.width())
        animation.setEndValue(0)
        animation.finished.connect(lambda: reset(hidden=True, defaultSize=defaultMaxWidth))

    animation.valueChanged.connect(changed)

    _start(animation, deletion, teardown)

    return animation


def expand(widget, duration: int = 250, deletion=None, teardown=None) -> QAbstractAnimation:
    return toggle_expansion(widget, True, duration, deletion, teardown)


def collapse(widget, duration: int = 250, deletion=None, teardown=None) -> QAbstractAnimation:
    return toggle_expansion(widget, False, duration, deletion, teardown)


def fade_in(widget, duration: int = 250, deletion=None, teardown=None) -> QAbstractAnimation:
    effect = QGraphicsOpacityEffect()
    __set_parent_if_qobj(effect, widget)

    widget.setVisible(True)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b'opacity')
    __set_parent_if_qobj(animation, widget)
    animation.setDuration(duration)
    animation.setStartValue(0)
    animation.setEndValue(1)
    animation.setEasingCurve(QEasingCurve.Type.InBack)
    _start(animation, deletion, teardown)

    return animation


def fade_out(widget, duration: int = 250, hide_if_finished: bool = True, deletion=None,
             teardown=None) -> QAbstractAnimation:
    effect = QGraphicsOpacityEffect()
    __set_parent_if_qobj(effect, widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b'opacity')
    __set_parent_if_qobj(animation, widget)
    animation.setDuration(duration)
    animation.setStartValue(1)
    animation.setEndValue(0)

    if hide_if_finished:
        animation.finished.connect(lambda: widget.setHidden(True))
    _start(animation, deletion, teardown)

    return animation


def glow(widget, duration: int = 200, radius: int = 8, loop: int = 1,
         color=QColor(Qt.red), deletion=None, startRadius: int = 0, reverseAnimation: bool = True, teardown=None) -> QAbstractAnimation:
    effect = QGraphicsDropShadowEffect()
    __set_parent_if_qobj(effect, widget)
    effect.setBlurRadius(startRadius)
    effect.setOffset(0)
    effect.setColor(color)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b'blurRadius')
    __set_parent_if_qobj(animation, widget)
    animation.setDuration(duration)
    animation.setStartValue(startRadius)
    animation.setEndValue(radius)

    if reverseAnimation:
        sequence = QSequentialAnimationGroup()
        __set_parent_if_qobj(sequence, widget)

        end_animation = reverse(animation)

        sequence.addAnimation(animation)
        sequence.addAnimation(end_animation)
        sequence.setLoopCount(loop)

        _start(sequence, deletion, teardown)
        return sequence
    else:
        _start(animation, deletion, teardown)
        return animation


def colorize(widget, duration: int = 200, strength: float = 0.5, loop: int = 1, color=QColor(Qt.red),
             deletion=None, teardown=None) -> QAbstractAnimation:
    effect = QGraphicsColorizeEffect()
    __set_parent_if_qobj(effect, widget)
    effect.setColor(color)
    widget.setGraphicsEffect(effect)

    sequence = QSequentialAnimationGroup(widget)

    animation = QPropertyAnimation(effect, b'strength')
    __set_parent_if_qobj(animation, widget)
    animation.setDuration(duration)
    animation.setStartValue(0)
    animation.setEndValue(strength)

    end_animation = reverse(animation)

    sequence.addAnimation(animation)
    sequence.addAnimation(end_animation)
    sequence.setLoopCount(loop)

    _start(sequence, deletion, teardown)

    return sequence


# class PaletteColorInterpolation(QWidget):
#     def __init__(self, palette: QPalette, widget: QWidget):
#         super(PaletteColorInterpolation, self).__init__(widget)
#         self.palette = palette
#         self.widget = widget
#
#     @Property(QColor)
#     def color(self) -> QColor:
#         return self.palette.color(QPalette.ButtonText)
#
#     @color.setter
#     def color(self, color: QColor):
#         self.palette.setColor(QPalette.ButtonText, color)
#         self.widget.setPalette(self.palette)


def pulse(widget, duration: int = 400, loop: int = 3, color=QColor(Qt.red),
          deletion=None, teardown=None) -> QAbstractAnimation:
    effect = QGraphicsDropShadowEffect()
    __set_parent_if_qobj(effect, widget)
    effect.setBlurRadius(0)
    effect.setOffset(0)
    effect.setColor(color)
    widget.setGraphicsEffect(effect)

    parallel = QParallelAnimationGroup(widget)

    shadow_animation = QPropertyAnimation(effect, b'blurRadius')
    __set_parent_if_qobj(shadow_animation, widget)
    shadow_animation.setDuration(duration // 2)
    shadow_animation.setStartValue(0)
    shadow_animation.setEndValue(8)

    reverse_shadow_animation = reverse(shadow_animation)

    shadow_sequence = QSequentialAnimationGroup()
    __set_parent_if_qobj(shadow_sequence, widget)
    shadow_sequence.addAnimation(shadow_animation)
    shadow_sequence.addAnimation(reverse_shadow_animation)

    original_size = widget.minimumSize()

    size_animation = QPropertyAnimation(widget, b'minimumSize')
    __set_parent_if_qobj(size_animation, widget)
    size_animation.setDuration(duration // 2)
    size_animation.setStartValue(widget.size())
    size = widget.size()
    size.setWidth(size.width() + 4)
    size.setHeight(size.height() + 4)
    size_animation.setEndValue(size)

    reverse_size_animation = reverse(size_animation)
    reverse_size_animation.setStartValue(size)
    reverse_size_animation.setEndValue(original_size)

    size_sequence = QSequentialAnimationGroup()
    __set_parent_if_qobj(size_sequence, widget)
    size_sequence.addAnimation(size_animation)
    size_sequence.addAnimation(reverse_size_animation)

    original_geo = widget.geometry()
    left_geo: QRect = widget.geometry()
    left_geo.setX(left_geo.x() - 2)
    left_geo.setY(left_geo.y() - 2)

    position_animation = QPropertyAnimation(widget, b'geometry')
    __set_parent_if_qobj(position_animation, widget)
    position_animation.setDuration(duration // 2)
    position_animation.setStartValue(original_geo)
    position_animation.setEndValue(left_geo)

    reverse_position_animation = reverse(position_animation)
    reverse_position_animation.setStartValue(left_geo)
    reverse_position_animation.setEndValue(original_geo)

    position_sequence = QSequentialAnimationGroup()
    __set_parent_if_qobj(position_sequence, widget)
    position_sequence.addAnimation(position_animation)
    position_sequence.addAnimation(reverse_position_animation)

    parallel.addAnimation(shadow_sequence)
    parallel.addAnimation(size_sequence)
    parallel.addAnimation(position_sequence)
    parallel.setLoopCount(loop)

    _start(parallel, deletion, teardown)

    return parallel


def _start(anim: QAbstractAnimation, deletion, teardown):
    if deletion is None:
        deletion = prop_anim_config.deletion_policy
    if teardown is not None:
        anim.finished.connect(lambda: teardown())
    anim.start(deletion)


def __set_parent_if_qobj(effect, widget):
    if isinstance(widget, QObject) and not isinstance(widget, QGraphicsObject):
        effect.setParent(widget)

# def shine(widget: QWidget) -> QAbstractAnimation:
#     widget.setStyleSheet(f'''
#         {widget.__class__.__name__} {{background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
#                                       stop: 0 #dadbde, stop: 0.7 white, stop: 1 #dadbde);}}
#     ''')
# gradient = QLinearGradient(widget.rect().x(), widget.rect().y(), widget.width(), widget.height())
# palette = QPalette()
# palette.setBrush(QPalette.ButtonText, QBrush(gradient))
# gradient.setColorAt(0, Qt.white)
# # gradient.setColorAt(0.5, Qt.red)
# gradient.setColorAt(1, Qt.blue)
# widget.setPalette(palette)
# effect = QGraphicsColorizeEffect(widget)
# widget.setGraphicsEffect(effect)
#
# animation = QPropertyAnimation(effect, b'color', widget)
# animation.setLoopCount(5)
# animation.setDuration(250)
# animation.setStartValue(QColor(Qt.GlobalColor.blue))
# animation.setEndValue(QColor(Qt.GlobalColor.red))
# animation.start(QPropertyAnimation.DeletionPolicy.KeepWhenStopped)
#
# return animation
