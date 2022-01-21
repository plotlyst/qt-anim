from qtpy.QtCore import QPropertyAnimation


def reverse(animation: QPropertyAnimation) -> QPropertyAnimation:
    reversed_animation = QPropertyAnimation(animation.targetObject(), animation.propertyName(), animation.parent())
    reversed_animation.setDuration(animation.duration())
    reversed_animation.setLoopCount(animation.loopCount())
    reversed_animation.setEasingCurve(animation.easingCurve())
    reversed_animation.setStartValue(animation.endValue())
    reversed_animation.setEndValue(animation.startValue())

    return reversed_animation
