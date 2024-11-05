from PySide2.QtGui import QGuiApplication
from PySide2.QtWidgets import QWidget


def update_ui_size(widget: QWidget, width_coe=0.5, height_coe=0.5):
    screen_geometry = QGuiApplication.primaryScreen().availableGeometry()

    # 计算窗口的宽度和高度为屏幕的一半
    window_width = screen_geometry.width() * width_coe
    window_height = screen_geometry.height() * height_coe

    # 设置窗口的几何信息（居中）
    widget.setGeometry(
        (screen_geometry.width() - window_width) // 2,
        (screen_geometry.height() - window_height) // 2,
        window_width,
        window_height,
    )
