from flet import Page, Theme, app
from os import fspath
from ui import App
from utils.path import FONT_PATH


def main(page: Page):
    page.fonts = {
        'msyh': fspath(FONT_PATH)
    }
    page.theme = Theme(
        font_family='msyh' 
    )
    page.window_width = 700
    page.window_height = 550
    page.padding = 0
    app = App(page)
    page.add(app)
    # page.title = 'ncm-downloader'
    app.init()
    page.window_center()   
    page.update()


# flet==0.17.0
# flet_core\page.py:471 ctrl.page = None 改为 if ctrl.page != self: ctrl.page = None
# 'https://github.com/flet-dev/examples/issues/102'
if __name__ == '__main__':
    app(target=main)