# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-09-19 11:29
# @Author : 毛鹏
from mango_ui import *
from mango_ui.init import *


class ContainerPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(MangoLabel('容器'))
