from mango_ui.models.models import ThemeConfig, AppConfig, MenusModel

THEME = ThemeConfig(**{
    "theme_name": "Default",
    "radius": "8",
    "border_size": "1",
    "dark_one": "#9d83a4",
    "dark_two": "#dad1dd",
    "dark_three": "#EDEDED",
    "dark_four": "#A8A8A8",
    "bg_one": "#ffffff",
    "bg_two": "#c2b2c6",
    "bg_three": "#A8A8A8",
    "d_color": "",
    "d_color_2": "",
    "d_color_3": "",
    "d_color_4": "",
    "d_color_5": "",
    "m1_color": "",
    "m1_color_2": "",
    "m1_color_3": "",
    "m1_color_4": "",
    "m1_color_5": "",
    "m2_color": "",
    "m2_color_2": "",
    "m2_color_3": "",
    "m2_color_4": "",
    "m2_color_5": "",
    "c_color": "",
    "c_color_2": "",
    "c_color_3": "",
    "c_color_4": "",
    "c_color_5": "",
    "icon_color": "#000000",
    "icon_hover": "#353037",
    "icon_pressed": "#626062",
    "icon_active": "#000000",
    "context_color": "#6db65a",
    "context_hover": "#c2b2c6",
    "context_pressed": "#a993af",
    "text_title": "#000000",
    "text_foreground": "#000000",
    "text_description": "#000000",
    "text_active": "#000000",
    "white": "#ffffff",
    "pink": "#FF82AB",
    "green": "#00FF7F",
    "red": "#EE3B3B",
    "yellow": "#fdb933",
    "blue": "#33a3dc",
    "orange": "#faa755",
    "font": {
        "family": "微软雅黑",
        "title_size": 11,
        "text_size": 10
    }
})

STYLE = AppConfig(**{
    "app_name": "芒果测试平台",
    "version": "v2.5.1",
    "copyright": "Copyright © By: 芒果味  2022-2024",
    "year": 2021,
    "theme_name": "mango",
    "custom_title_bar": True,
    "startup_size": [
        1200,
        800
    ],
    "minimum_size": [
        960,
        640
    ],
    "lef_menu_size": {
        "minimum": 50,
        "maximum": 240
    },
    "left_menu_content_margins": 3,
    "left_column_size": {
        "minimum": 0,
        "maximum": 240
    },
    "right_column_size": {
        "minimum": 0,
        "maximum": 240
    },
    "time_animation": 500,
    "font": {
        "family": "微软雅黑",
        "title_size": 11,
        "text_size": 10
    }
})

MENUS = MenusModel(**{
    "left_menus": [
        {
            "btn_icon": ":/icons/home.svg",
            "btn_id": "home",
            "btn_text": "首页",
            "btn_tooltip": "首页",
            "show_top": True,
            "is_active": True
        },
        {
            "btn_icon": ":/icons/app_icon.svg",
            "btn_id": "layout",
            "btn_text": "布局",
            "btn_tooltip": "布局",
            "show_top": True,
            "is_active": False,
            "submenus": [
                {
                    "btn_icon": ":/icons/mind-mapping.svg",
                    "btn_id": "page",
                    "btn_text": "布局1",
                    "btn_tooltip": "布局1",
                    "show_top": True,
                    "is_active": False
                },
                {
                    "btn_icon": ":/icons/mind-mapping.svg",
                    "btn_id": "page",
                    "btn_text": "布局2",
                    "btn_tooltip": "布局2",
                    "show_top": True,
                    "is_active": False
                },

            ]
        },
        {
            "btn_icon": ":/icons/calendar_clock.svg",
            "btn_id": "input",
            "btn_text": "输入",
            "btn_tooltip": "输入",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/command.svg",
            "btn_id": "feedback",
            "btn_text": "反馈",
            "btn_tooltip": "反馈消息",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/compass.svg",
            "btn_id": "component",
            "btn_text": "反馈",
            "btn_tooltip": "反馈消息",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/down.svg",
            "btn_id": "container",
            "btn_text": "容器",
            "btn_tooltip": "容器",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/fill.svg",
            "btn_id": "charts",
            "btn_text": "图表",
            "btn_tooltip": "图表",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/home.svg",
            "btn_id": "display",
            "btn_text": "显示",
            "btn_tooltip": "显示",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/icon_add_user.svg",
            "btn_id": "graphics",
            "btn_text": "图形",
            "btn_tooltip": "图形",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/icon_arrow_left.svg",
            "btn_id": "menu",
            "btn_text": "菜单",
            "btn_tooltip": "菜单",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/icon_arrow_right.svg",
            "btn_id": "window",
            "btn_text": "窗口",
            "btn_tooltip": "窗口",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": ":/icons/icon_info.svg",
            "btn_id": "其他",
            "btn_text": "菜单",
            "btn_tooltip": "菜单",
            "show_top": True,
            "is_active": False
        },

    ],
    "title_bar_menus": [
        {
            "btn_icon": ":/icons/icon_search.svg",
            "btn_id": "btn_search",
            "btn_tooltip": "搜索",
            "is_active": False
        }
    ]
})
