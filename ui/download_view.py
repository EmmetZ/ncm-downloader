from flet import (
    UserControl,
    Container,
    Row,
    Column,
    Text,
    margin,
    border,
    border_radius,
    colors,
    ElevatedButton,
    SnackBar,
    Page
)


class DownloadView(UserControl):
    def __init__(self, app, page: Page):
        super().__init__()
        self.app = app
        self.page = page
        self.log = ''


    def init(self, info):
        self.num = info[0]
        self.numLabel = Text(
            value=f'0/{info[0]}'
        )
        self.coverLabel = Text(
            value=f'下载封面：{info[1]}'
        )
        self.lyricLabel = Text(
            value=f'下载歌词：{info[2]}'
        )


    def build(self):
        self.logView = Column(
            controls=[],
            width=self.app.page.width-5,
            height=self.app.page.height-56-5-65,
            scroll='auto',
            auto_scroll=True
        )
        self.getLogButton = ElevatedButton(
            text='导出记录',
            disabled=True,
            on_click=self.getLog,
            height=30
        )
        self.view = Container(
            content=Column(
                controls=[
                    Row(
                        controls=[
                            Container(width=15),
                            self.numLabel,
                            Container(width=10),
                            self.coverLabel,
                            Container(width=10),
                            self.lyricLabel,
                            Container(width=10),
                            self.getLogButton
                        ],
                        width=self.app.page.width-5,
                    ),
                    Container(
                        content=self.logView,
                        border=border.all(2, color=colors.GREY),
                        border_radius=border_radius.all(10),
                        margin=margin.only(left=10, right=10),
                    ),
                ],
                width=self.app.page.width-5,
                scroll='auto'
            ),
            width=self.app.page.width,
            height=self.app.page.height-56-15-5,
            margin=margin.only(top=15, bottom=5),
        )
        self.page.snack_bar = SnackBar(content=Text(value='保存成功'))
        return self.view


    def add(self, title, mes):
        if '[download]' in mes:
            currNum = int(self.numLabel.value.split("/")[0])+1
            self.numLabel.value = f'{currNum}/{self.num}'
        item = Row(
            controls=[
                Container(width=15),
                Text(
                    value=f'{title}: {mes}',
                    width=self.app.page.width-5,
                )
            ]
        )
        self.logView.controls.append(item)
        self.view.update()
        self.log += f'{title}: {mes}\n'


    def finish(self, savepath):
        self.savepath = savepath
        self.getLogButton.disabled = False
        self.add('\n下载完成!', f'保存路径：{self.savepath}\n')
    

    def getLog(self, e):
        f = open(self.savepath.joinpath('log.txt'), 'w+', encoding='utf-8')
        f.write(self.log)
        f.close()
        self.page.snack_bar.open = True
        self.page.update()