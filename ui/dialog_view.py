from flet import (
    Page,
    AlertDialog,
    TemplateRoute,
    Text,
    ElevatedButton,
    Container,
    Column,
    colors,
    FontWeight,
    alignment,
    Row,
    Image,
    ImageFit
)


def info(page: Page, e):
    def closeDialog(e):
        dialog.open = False
        page.update()

    route = TemplateRoute(page.route)
    clsButton = ElevatedButton(
        text='ok',
        on_click=closeDialog,
        disabled=False,
    )
    dialog = AlertDialog(
        title=Text(
            value='帮助',
            color=colors.BLACK,
            size=30,
            weight=FontWeight.BOLD,
        )
    )
    if route.match('/start'):
        dialog.content = startDialog(clsButton)
        page.dialog = dialog
        page.dialog.open = True
    elif route.match('/check'):
        dialog.content = checkDialog(clsButton)
        page.dialog = dialog
        page.dialog.open = True
    elif route.match('/download'):
        dialog.content = downloadDialog(clsButton)
        page.dialog = dialog
        page.dialog.open = True
    page.update()


def startDialog(clsButton):
    c = Container(
        content=Column(
            controls=[
                Text(
                    value='请输入网易云音乐歌单/单曲/专辑链接',
                ),
                Text(
                    '示例：\nhttps://music.163.com/#/playlist?id=123456&userid=123456\nhttps://music.163.com/#/song?id=123456&userid=123456\nhttps://music.163.com/#/album?id=123456&userid=123456\n* 必须有id\n只能下载非vip歌曲！！！收听vip歌曲请支持官方正版！！！',
                    selectable=False
                ),
                Text(
                    value='登陆说明：',
                    weight=FontWeight.BOLD,
                ),
                Text(
                    value='未登录时，歌单只能获取前10首，登陆后，非个人歌单只能获取前20首，一次最多获取1000首歌\n如遇到不能下载的情况，请登陆后再次尝试'
                ),
                Text(
                    value='有关下载和登陆的更多信息，请查看仓库：'
                ),
                Row(
                    controls=[
                        Container(
                            content=Text(
                                value='GitHub pyncm',
                                color=colors.BLUE_700,
                            ),
                            url='https://github.com/mos9527/pyncm',
                            url_target='_blank',
                        ),
                        Container(
                            content=clsButton,
                            alignment=alignment.center_right,
                            width=450
                        )
                    ]
                )
            ],
            height=350
        )
    )
    return c


def checkDialog(clsButton):
    c = Container(
        content=Column(
            controls=[
                Text(
                    value='下载说明：',
                    weight=FontWeight.BOLD,
                ),
                Text(
                    value='未找到资源的歌曲无法下载，如果歌单显示不全，请登陆后再次尝试或确认是否是个人歌单'
                ),
                Text(
                    value='高级设置：(下载时间增加)\n1. 封面下载：下载专辑封面并写入歌曲文件中\n2. 歌词下载：下载.lrc歌词文件，包括原歌词，翻译后的歌词(_tlrc)和罗马音歌词(_rlrc)(如果有歌词的话)'
                ),
                Text(
                    value='返回主菜单将清除歌曲下载设置'
                ),
                Container(
                    content=clsButton,
                    alignment=alignment.center_right,
                )
            ],
            height=240
        )
    )
    return c


def downloadDialog(clsButton):
    c = Container(
        content=Column(
            controls=[
                Text(
                    value='返回上一级菜单将保留歌曲下载设置'
                ),
                Text(
                    value='同一文件夹下，歌曲不重复下载'
                ),
                Container(
                    content=clsButton,
                    alignment=alignment.center_right
                )
            ]
        ),
        height=100
    )
    return c


def showQrcode(page: Page, base64Img):
    def closeDialog(e):
        dialog.open = False
        page.update()

    clsButton = ElevatedButton(
        text='ok',
        on_click=closeDialog,
        disabled=False,
    )
    dialog = AlertDialog(
        content=Column(
            controls=[
                Text(
                    value='请使用网易云音乐扫描二维码登陆',
                    size=20
                ),
                Container(
                    content=Image(
                        src_base64=base64Img,
                        fit=ImageFit.CONTAIN,
                        width=300,
                        height=300
                    ),
                ),
                Container(
                    content=clsButton,
                    alignment=alignment.center_right
                )
            ]
        ),
        modal=True
    )
    page.dialog = dialog
    dialog.open = True
    page.update()
