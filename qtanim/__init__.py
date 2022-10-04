from qtpy.QtCore import QPropertyAnimation
from qtpy.QtCore import Qt, QRect, QSequentialAnimationGroup, QEasingCurve, QParallelAnimationGroup, \
    QAbstractAnimation
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QGraphicsColorizeEffect, QGraphicsOpacityEffect, QGraphicsDropShadowEffect
from qtpy.QtWidgets import QWidget

from qtanim.util import reverse


def flash(widget: QWidget, start_color: QColor = QColor(Qt.blue),
          end_color: QColor = QColor(Qt.red),
          deletion=QPropertyAnimation.DeletionPolicy.KeepWhenStopped) -> QAbstractAnimation:
    effect = QGraphicsColorizeEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b'color', widget)
    animation.setLoopCount(5)
    animation.setDuration(250)
    animation.setStartValue(start_color)
    animation.setEndValue(end_color)

    animation.start(deletion)
    animation.finished.connect(lambda: widget.setGraphicsEffect(None))

    return animation


def shake(widget: QWidget, distance: int = 5, loop: int = 3,
          deletion=QPropertyAnimation.DeletionPolicy.KeepWhenStopped) -> QAbstractAnimation:
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

    sequence.start(deletion)

    return sequence


def fade_in(widget: QWidget, duration: int = 250,
            deletion=QPropertyAnimation.DeletionPolicy.KeepWhenStopped) -> QAbstractAnimation:
    effect = QGraphicsOpacityEffect(widget)
    widget.setVisible(True)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b'opacity', widget)
    animation.setDuration(duration)
    animation.setStartValue(0)
    animation.setEndValue(1)
    animation.setEasingCurve(QEasingCurve.Type.InBack)
    animation.start(deletion)

    return animation


def fade_out(widget: QWidget, duration: int = 250, hide_if_finished: bool = True,
             deletion=QPropertyAnimation.DeletionPolicy.KeepWhenStopped) -> QAbstractAnimation:
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b'opacity', widget)
    animation.setDuration(duration)
    animation.setStartValue(1)
    animation.setEndValue(0)

    if hide_if_finished:
        animation.finished.connect(lambda: widget.setHidden(True))
    animation.start(deletion)

    return animation


def glow(widget: QWidget, duration: int = 200, radius: int = 8, loop: int = 1,
         color: QColor = QColor(Qt.red),
         deletion=QPropertyAnimation.DeletionPolicy.KeepWhenStopped) -> QAbstractAnimation:
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(0)
    effect.setOffset(0)
    effect.setColor(color)
    widget.setGraphicsEffect(effect)

    sequence = QSequentialAnimationGroup(widget)

    animation = QPropertyAnimation(effect, b'blurRadius', widget)
    animation.setDuration(duration)
    animation.setStartValue(0)
    animation.setEndValue(radius)

    end_animation = reverse(animation)

    sequence.addAnimation(animation)
    sequence.addAnimation(end_animation)
    sequence.setLoopCount(loop)

    sequence.start(deletion)

    return sequence


def colorize(widget, duration: int = 200, strength: float = 0.5, loop: int = 1, color: QColor = QColor(Qt.red),
             deletion=QPropertyAnimation.DeletionPolicy.KeepWhenStopped) -> QAbstractAnimation:
    effect = QGraphicsColorizeEffect(widget)
    effect.setColor(color)
    widget.setGraphicsEffect(effect)

    sequence = QSequentialAnimationGroup(widget)

    animation = QPropertyAnimation(effect, b'strength', widget)
    animation.setDuration(duration)
    animation.setStartValue(0)
    animation.setEndValue(strength)

    end_animation = reverse(animation)

    sequence.addAnimation(animation)
    sequence.addAnimation(end_animation)
    sequence.setLoopCount(loop)

    sequence.start(deletion)

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


def pulse(widget: QWidget, duration: int = 400, loop: int = 3, color: QColor = QColor(Qt.red),
          deletion=QPropertyAnimation.DeletionPolicy.KeepWhenStopped) -> QAbstractAnimation:
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(0)
    effect.setOffset(0)
    effect.setColor(color)
    widget.setGraphicsEffect(effect)

    parallel = QParallelAnimationGroup(widget)

    shadow_animation = QPropertyAnimation(effect, b'blurRadius', widget)
    shadow_animation.setDuration(duration // 2)
    shadow_animation.setStartValue(0)
    shadow_animation.setEndValue(8)

    reverse_shadow_animation = reverse(shadow_animation)

    shadow_sequence = QSequentialAnimationGroup(widget)
    shadow_sequence.addAnimation(shadow_animation)
    shadow_sequence.addAnimation(reverse_shadow_animation)

    original_size = widget.minimumSize()

    size_animation = QPropertyAnimation(widget, b'minimumSize', widget)
    size_animation.setDuration(duration // 2)
    size_animation.setStartValue(widget.size())
    size = widget.size()
    size.setWidth(size.width() + 4)
    size.setHeight(size.height() + 4)
    size_animation.setEndValue(size)

    reverse_size_animation = reverse(size_animation)
    reverse_size_animation.setStartValue(size)
    reverse_size_animation.setEndValue(original_size)

    size_sequence = QSequentialAnimationGroup(widget)
    size_sequence.addAnimation(size_animation)
    size_sequence.addAnimation(reverse_size_animation)

    original_geo = widget.geometry()
    left_geo: QRect = widget.geometry()
    left_geo.setX(left_geo.x() - 2)
    left_geo.setY(left_geo.y() - 2)

    position_animation = QPropertyAnimation(widget, b'geometry', widget)
    position_animation.setDuration(duration // 2)
    position_animation.setStartValue(original_geo)
    position_animation.setEndValue(left_geo)

    reverse_position_animation = reverse(position_animation)
    reverse_position_animation.setStartValue(left_geo)
    reverse_position_animation.setEndValue(original_geo)

    position_sequence = QSequentialAnimationGroup(widget)
    position_sequence.addAnimation(position_animation)
    position_sequence.addAnimation(reverse_position_animation)

    parallel.addAnimation(shadow_sequence)
    parallel.addAnimation(size_sequence)
    parallel.addAnimation(position_sequence)
    parallel.setLoopCount(loop)

    parallel.start(deletion)

    return parallel

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
