# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time   : 2024-08-16 17:05
# @Author : 毛鹏
from PySide6.QtWidgets import QVBoxLayout

from mango_ui.init import QStackedWidget, QApplication, QMetaObject, Qt
from mango_ui.settings.settings import THEME
from mango_ui.widgets.display.mango_label import MangoLabel


class PagesWindow:

    def __init__(self, central_widget, loop):
        self.central_widget = central_widget
        self.loop = loop
        self.loading_indicator = self.create_loading_indicator()

    def create_loading_indicator(self):
        loading_indicator = MangoLabel("数据加载中...")
        loading_indicator.setAlignment(Qt.AlignCenter)
        loading_indicator.setStyleSheet(f"font-size: 16px; color: {THEME.icon_color};")
        return loading_indicator

    def setup_ui(self, main_window, page_dict):
        self.main_pages_layout = QVBoxLayout(main_window)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setContentsMargins(0, 0, 0, 0)
        self.pages = QStackedWidget(main_window)
        self.main_pages_layout.addWidget(self.pages)

        self.page_dict = page_dict
        self.pages.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(main_window)

    def set_page(self, page: str, data: dict | None = None):
        self.pages.addWidget(self.loading_indicator)
        self.pages.setCurrentWidget(self.loading_indicator)
        QApplication.processEvents()

        page_class = self.page_dict.get(page)
        if page_class is not None:
            page = page_class(self)
        else:
            return
        current_widget = self.pages.currentWidget()
        if current_widget and current_widget != self.loading_indicator:
            self.pages.removeWidget(current_widget)
        if data is not None and isinstance(data, dict):
            page.data = data
        else:
            page.data = {}
        if hasattr(page, 'show_data'):
            page.show_data()
        self.pages.addWidget(page)
        self.pages.setCurrentWidget(page)
        self.pages.removeWidget(self.loading_indicator)
