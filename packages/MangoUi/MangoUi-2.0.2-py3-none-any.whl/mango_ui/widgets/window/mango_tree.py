# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-10-29 11:25
# @Author : 毛鹏
from typing import Optional

from mango_ui.models.models import TreeModel
from mango_ui.init import *


class MangoTree(QTreeWidget):
    clicked = Signal(TreeModel)

    def __init__(self,
                 title: str,
                 parent=None):
        super().__init__(parent)
        self.data: Optional[list[TreeModel] | None] = None
        self.setHeaderLabels([title])
        self.itemClicked.connect(self.on_item_clicked)
        self.set_stylesheet()

    def on_item_clicked(self, item, column):
        if item.childCount() > 0:
            item.setExpanded(not item.isExpanded())
        else:
            self.clicked.emit(item.data(0, Qt.UserRole))  # type: ignore

    def set_item(self, items: list[TreeModel]):
        self.data = items
        for item in items:
            parent_item = QTreeWidgetItem(self)
            parent_item.setText(0, item.title)
            parent_item.setData(0, Qt.UserRole, item)  # type: ignore
            if item.children:
                for i in item.children:
                    child_item = QTreeWidgetItem(parent_item)
                    child_item.setText(0, i.title)  # type: ignore
                    child_item.setData(0, Qt.UserRole, i)  # type: ignore

    def set_stylesheet(self):
        style = f"""
            MangoTree {{
                background-color: {THEME.white};
                border-radius: {THEME.radius}px;
                border: {THEME.border_size}px solid gray;
                color: {THEME.text_foreground};
            }}
        
            MangoTree::item {{
                padding: 5px;
                background-color: {THEME.white};
                color: {THEME.text_foreground};
            }}
        
            MangoTree::item:selected {{
                background-color: {THEME.context_color};
                color: {THEME.white};
            }}
        
            MangoTree::item:hover {{
                background-color: {THEME.dark_three};
            }}
            QHeaderView {{
                font-size: 14px;  /* 修改字体大小 */

            }}
        """
        self.setStyleSheet(style)
