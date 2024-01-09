from flet import(
    Page,
    UserControl,
    View,
    Container,
    Text,
    colors,
    AppBar,
    IconButton,
    icons,
    TemplateRoute,
    padding,
)
from os import fspath
from time import sleep
from functools import partial

from ui.app_layout import AppLayout
from ui.download_view import DownloadView
from ui.dialog_view import info
from utils.client import Clinet
from utils.music import Music


class App(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.client = Clinet()
        self.backButton = IconButton(
            icon=icons.MUSIC_NOTE,
            icon_color=colors.RED_700,
            icon_size=30,
            disabled=True,
            on_click=self.setPreView
        )
        self.appbar = AppBar(
            leading=self.backButton,
            title=Text('ncm-downloader', text_align='start'),
            actions=[
                IconButton(
                    icon=icons.HELP_OUTLINE,
                    tooltip='帮助',
                    on_click=partial(info, self.page)
                ),
                Container(width=10)
            ],
            bgcolor=colors.RED_200, 
        ) 
        self.page.on_route_change = self.routeChange
        self.page.appbar = self.appbar
        self.width = 700


    def build(self):
        self.layout = AppLayout(self, self.page)
        return self.layout


    def init(self):
        self.page.views.clear()
        self.page.views.append(
            View(
                "/",
                [self.appbar, self.layout],
                padding=padding.all(0)
            )
        )
        self.page.update()
        self.page.go('/')


    def routeChange(self, e):
        route = TemplateRoute(self.page.route)
        if route.match('/'):
            self.page.go('/start')
        elif route.match('/start'):
            self.ChangeLeading(route)
        elif route.match('/check'):
            self.ChangeLeading(route)
            flag = self.layout.setCheckView(
                self.client.count,
                self.client.coverFlag,
                self.client.lyricFlag
            )
            if flag:
                self.client.getMusicList()
            self.layout.checkView.setMusicList(self.client.musicList)
        elif route.match('/download'):
            for i in range(len(self.layout.checkView.musicList)):
                self.client.musicList[i].downloadFlag = self.layout.checkView.entryList[i].selectFlag
            self.client.coverFlag = self.layout.checkView.coverSwitch.value
            self.client.lyricFlag = self.layout.checkView.lyricSwitch.value
            self.layout.setDownloadView()
            self.client.setPath()
            Music.setParams(
                savepath=self.client.savepath,
                cover=self.layout.downloadView.coverLabel,
                lyric=self.layout.downloadView.lyricLabel,
                downloadView=self.layout.downloadView
            )
            self.client.download(self.layout.downloadView.num)
            self.layout.downloadView.finish(self.client.savepath)


    def ChangeLeading(self, route: TemplateRoute):
        if route.match('/check'):
            self.backButton.disabled = False
            self.backButton.icon = icons.ARROW_BACK
            self.backButton.icon_color = colors.BLACK
            self.backButton.tooltip = '返回'
        elif route.match('/start'): 
            self.backButton.disabled = True
            self.backButton.icon = icons.MUSIC_NOTE
            self.backButton.icon_color = colors.RED
            self.backButton.tooltip = ''


    def setPreView(self, e):
        route = TemplateRoute(self.page.route)
        if route.match('/check'):
            sleep(0.1)
            self.page.go('/start')
            self.layout.setStartView()
        elif route.match('/download'):
            sleep(0.1)
            self.page.go('/check')

