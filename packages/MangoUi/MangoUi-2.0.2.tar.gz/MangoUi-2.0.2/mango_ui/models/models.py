# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: 
# @Time   : 2024-10-08 16:15
# @Author : 毛鹏
from typing import Any

from pydantic import BaseModel

from mango_ui.enums.enums import InputEnum


class ResponseModel(BaseModel):
    code: int
    msg: str
    data: list[dict] | dict | None = None
    totalSize: int | None = None


class Font(BaseModel):
    family: str
    title_size: int
    text_size: int


class LeftMenuSize(BaseModel):
    minimum: int
    maximum: int


class ColumnSize(BaseModel):
    minimum: int
    maximum: int


class AppConfig(BaseModel):
    app_name: str
    version: str
    copyright: str
    year: int
    theme_name: str
    custom_title_bar: bool
    startup_size: list[int]
    minimum_size: list[int]
    lef_menu_size: LeftMenuSize
    left_menu_content_margins: int
    left_column_size: ColumnSize
    right_column_size: ColumnSize
    time_animation: int
    font: Font


class ThemeConfig(BaseModel):
    theme_name: str
    dark_one: str
    dark_two: str
    dark_three: str
    dark_four: str
    bg_one: str
    bg_two: str
    bg_three: str
    icon_color: str
    icon_hover: str
    icon_pressed: str
    icon_active: str
    context_color: str
    context_hover: str
    context_pressed: str
    text_title: str
    text_foreground: str
    text_description: str
    text_active: str
    white: str
    pink: str
    green: str
    red: str
    yellow: str
    blue: str
    orange: str
    radius: str
    border_size: str
    font: Font


class LeftMenuModel(BaseModel):
    btn_icon: str
    btn_id: str
    btn_text: str
    btn_tooltip: str
    show_top: bool
    is_active: bool
    is_active: bool
    submenus: list['LeftMenuModel'] = []
    url: str | None = None


class TitleBarMenusModel(BaseModel):
    btn_icon: str
    btn_id: str
    btn_tooltip: str
    is_active: bool


class MenusModel(BaseModel):
    left_menus: list[LeftMenuModel]
    title_bar_menus: list[TitleBarMenusModel]


class SearchDataModel(BaseModel):
    title: str
    placeholder: str
    key: str
    type: InputEnum = InputEnum.INPUT
    select: dict | list[dict] | Any = None
    input_object: None = None
    value: str | None = None
    subordinate: str | None = None  # 是否联动下级选择条件


class RightDataModel(BaseModel):
    name: str
    theme: str
    action: str
    obj: Any | None = None


class FormDataModel(BaseModel):
    title: str
    placeholder: str
    key: str
    input_object: None = None
    value: str | None = None
    type: InputEnum = InputEnum.INPUT
    select: dict | list[dict] | Any = None  # 选项数据
    subordinate: str | None = None  # 是否联动下级选择条件
    required: bool = True  # 是否必填


class TableColumnModel(BaseModel):
    key: str
    name: str
    width: int | None = None
    option: dict | list[dict] | None = None


class TableMenuItemModel(BaseModel):
    name: str
    action: str
    son: list['TableMenuItemModel'] = []


class FieldListModel(BaseModel):
    key: str
    name: str


class CascaderModel(BaseModel):
    value: int | str
    label: str
    parameter: dict | None = None
    children: list['CascaderModel'] = []


class TreeModel(BaseModel):
    key: str
    status: int
    title: str
    children: list['TreeModel'] = []


class DialogCallbackModel(BaseModel):
    key: str | None = None
    value: int | str | None
    input_object: Any | None = None
    subordinate: str
    subordinate_input_object: Any | None = None


class ComboBoxDataModel(BaseModel):
    id: int | str | None
    name: str | None
