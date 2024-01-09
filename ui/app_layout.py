from flet import (
    Column,
    Page,
    Row,
    Container,
    Text,
    colors,
    TextField,
    IconButton,
    icons,
    TextStyle,
    TextTheme,
    Theme,
    FilePicker,
    FilePickerResultEvent,
    MainAxisAlignment,
)
import re
import time

from ui.check_view import CheckView
from ui.download_view import DownloadView
from ui.dialog_view import showQrcode
from utils.path import BASE_FILEPATH

class AppLayout(Row):
    def __init__(self, app, page: Page):
        super().__init__()
        self.app = app
        self.page = page
        self.checkView = None
        self.downloadView = None
        self.urlTestfield = TextField(
            label='输入链接',
            hint_text='输入单曲/歌单链接',
            on_change=self.textfieldChange,
            prefix_icon=icons.LINK,
            width=550,
            autofocus=True
        )
        self.clrButton = IconButton(
            icon=icons.DELETE,
            on_click=self.clear,
            disabled=True,
            icon_size=35,
            icon_color=colors.GREY,
            tooltip='清空',
        ) 
        self.startButton = IconButton(
            icon=icons.SEARCH,
            disabled=True,
            icon_color=colors.GREY,
            icon_size=35,
            tooltip='搜索',
            on_click=self.start
        )
        self.tip = Text(value=' ')
        self.anonymousLoginButton = IconButton(
            icon=icons.PERSON,
            icon_size=35,
            tooltip='匿名登陆',
            icon_color=colors.BLACK,
            on_click=self.anonymousLogin
        )
        self.qrcodeLoginButton = IconButton(
            icon=icons.QR_CODE,
            icon_size=35,
            tooltip='扫码登陆',
            icon_color=colors.BLACK,
            on_click=self.qrcodeLogin
        )
        self.loginInfo = Text(value='未登陆')
        self.filePickerDialog = FilePicker(
            on_result=self.setFilePath
        )
        self.filePickerButton = IconButton(
            icon=icons.FOLDER_OPEN_OUTLINED,
            on_click=lambda _:self.filePickerDialog.get_directory_path(
                dialog_title='选择文件夹',
            ),
            icon_size=30,
            icon_color=colors.YELLOW_700,
            tooltip='选择文件夹'
        )
        self.fileLabel = Text(value=' ')
        self.page.overlay.append(self.filePickerDialog)

        self.startView = Container(
            content=Column(
                controls=[
                    Container(
                        width=100,
                        height=60,
                    ), # divider
                    Row(
                        controls=[
                            self.urlTestfield,
                            self.startButton
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        width=self.app.width
                    ),
                    Row(
                        controls=[
                            Container(
                                width=50,
                                height=5,
                            ),
                            self.tip,
                            Container(
                                width=20,
                            ),
                            self.fileLabel
                        ]
                    ),
                    Row(
                        controls=[
                            self.anonymousLoginButton,
                            Container(
                                width=20,
                            ),
                            self.qrcodeLoginButton,
                            Container(
                                width=20,
                            ),
                            self.filePickerButton,
                            Container(
                                width=20,
                            ),
                            self.clrButton
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        width=self.app.width
                    ),
                    Row(
                        controls=[
                            Container(
                                width=90,
                                height=20,
                            ),
                        ]
                    ),
                    Container(
                        width=100,
                        height=20,
                    ), # divider
                    Row(
                        controls=[
                            Container(
                                width=50,
                                height=20,
                            ),
                            Text(value='登陆状态: '),
                            self.loginInfo
                        ]
                    )
                ],
            ),
            theme=Theme(text_theme=TextTheme(label_large=TextStyle(size=18, font_family='msyh')))
        )


        self._acviteView = self.startView
        self.controls = [self.activeView]


    def clear(self, e):
        if self.urlTestfield.value != "":
            self.urlTestfield.value = ""
            self.tip.value = " "
            self.clrButton.disabled = True
            self.clrButton.icon_color = colors.GREY
            self.startButton.disabled = True
            self.startButton.icon_color = colors.GREY
            self.urlTestfield.focus()
            self.page.update()


    def textfieldChange(self, e):
        if self.urlTestfield.value == "":
            self.clrButton.disabled = True
            self.clrButton.icon_color = colors.GREY
            self.startButton.disabled = True
            self.startButton.icon_color = colors.GREY
            self.tip.value = " "
        else:
            self.clrButton.disabled = False
            self.clrButton.icon_color = colors.RED
            self.tip.value = '正在检查链接...'
            self.page.update()
            label, id = self.match(self.urlTestfield.value)
            if label != 'false':
                category, name = self.app.client.search(label, id)
                self.tip.value = f'{category}: {name}'
                self.startButton.disabled = False
                self.startButton.icon_color = colors.BLUE
            else:
                self.tip.value = '链接格式错误'
        self.page.update()


    def start(self, e):
        time.sleep(0.1)
        self.page.go('/check')


    def setStartView(self):
        self.fileLabel.value = ' '
        self.activeView = self.startView
        del self.checkView
        del self.downloadView
        self.checkView = None
        self.downloadView = None
        self.app.client.coverFlag = False
        self.app.client.lyricFlag = False
        self.app.client.savepath = BASE_FILEPATH
        self.page.update()


    def setCheckView(self, count, cover, lyric) -> bool:
        flag = False
        if self.checkView == None:
            self.checkView = CheckView(self.app, count, cover, lyric)
            flag = True
        self.activeView = self.checkView
        self.page.update()
        return flag

    
    def setDownloadView(self):
        self.downloadView = DownloadView(self.app, self.page)
        self.downloadView.init(self.checkView.transfer())
        self.activeView = self.downloadView
        self.page.update()


    def match(self,url) -> tuple[str]:
        # https://music.163.com/playlist?id=5148785723&userid=1749319431
        # https://music.163.com/song?id=1992712131&userid=1749319431
        # https://music.163.com/album?id=153778832&userid=1749319431
        # https://music.163.com/album?id=80440087&userid=1749319431
        pattern = r"https://music.163.com/(\S+)\?id=(\d+)"
        res = re.search(pattern, url)
        if res:
            label = res.group(1)
            id = res.group(2)
            return label, id
        else:
            return 'false', '0' 

    
    def setFilePath(self, e: FilePickerResultEvent):
        if e.path != None:
            self.fileLabel.value = f'保存路径: {e.path}'
            self.app.client.savepath = e.path
            self.page.update()
    

    def anonymousLogin(self, e):
        if self.loginInfo.value != '匿名登陆':
            self.qrcodeLoginButton.disabled = True
            self.anonymousLoginButton.icon = icons.REFRESH
            self.anonymousLoginButton.disabled = True
            self.page.update()
            info = self.app.client.anonymousLogin()
            self.qrcodeLoginButton.disabled = False
            self.anonymousLoginButton.icon = icons.PERSON
            self.anonymousLoginButton.disabled = False
            self.setLoginInfo(info)
    

    def qrcodeLogin(self, e):
        self.anonymousLoginButton.disabled = True
        self.qrcodeLoginButton.icon = icons.REFRESH
        self.qrcodeLoginButton.disabled = True
        self.qrcodeLoginButton.tooltip = '正在登陆'
        self.page.update()
        img = self.app.client.getQrcode()
        showQrcode(self.page, img)
        info = self.app.client.loginCheck()
        if hasattr(self.page, 'dialog') and self.page.dialog.open == True:
            self.page.dialog.open = False
            self.page.update()
        self.qrcodeLoginButton.icon = icons.QR_CODE
        self.qrcodeLoginButton.disabled = False
        self.anonymousLoginButton.disabled = False
        self.qrcodeLoginButton.tooltip = '扫码登陆'
        self.setLoginInfo(info)


    def setLoginInfo(self, info: dict):
        if info['code'] == 200 and info['account'] != None: 
            account = info['account']
            if account['anonimousUser'] == True:
                self.loginInfo.value = '匿名登陆'
            else:
                self.loginInfo.value = f'登陆成功：{account["userName"]}'
        elif info['code'] == 200 and info['account'] == None:
            self.loginInfo.value = '未登陆'
        elif info['code'] == 500:
            self.loginInfo.value = '登陆超时'
        else:
            self.loginInfo.value = '登陆失败，请重试'
        self.textfieldChange(None)
        self.page.update()


    @property
    def activeView(self):
        return self._acviteView
    
    @activeView.setter
    def activeView(self, view):
        self._acviteView = view
        self.controls[-1] = self._acviteView
        self.page.update()