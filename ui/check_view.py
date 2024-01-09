from flet import(
    UserControl,
    Container,
    Column,
    Row,
    Checkbox,
    Text,
    Chip,
    colors,
    margin,
    CupertinoSwitch,
    ElevatedButton,
    icons,
    ProgressRing,
    alignment,
    ControlEvent,
    PopupMenuButton,
    PopupMenuItem,
)
import re
from itertools import count

from utils.music import Music
from ui.music_entry import MusicEntry


class CheckView(UserControl):
    def __init__(self, app, count, cover, lyric):
        super().__init__()
        self.app = app
        self.count = count
        self.coverSwitch = CupertinoSwitch(
            label='  下载封面',
            value=cover
        )
        self.lyricSwitch = CupertinoSwitch(
            label='  下载歌词',
            value=lyric
        )


    def build(self):
        self.selectAllCheckbox = Checkbox(
            label='全选',
            value=True,
            on_change=self.selectAll,
            disabled=True
        )
        self.numLabel = Text(
            value=f'_/({self.count})'
        ) 
        self.sizeLabel = Text(
            value='_MB'
        )
        self.resFoundChip = Chip(
            label=Text('已找到'),
            selected_color=colors.GREEN_200,
            on_select=self.showEntry,
            selected=True,
            disabled=True
        )
        self.noneFoundChip = Chip(
            label=Text('未找到'),
            selected_color=colors.GREEN_200,
            on_select=self.showEntry,
            selected=False,
            disabled=True  
        )
        self.downloadButton = ElevatedButton(
            text='下载',
            icon=icons.PLAY_ARROW,
            icon_color=colors.GREEN,
            on_click=self.download,
            disabled=True
        )
        self.settingsButton = PopupMenuButton(
            icon=icons.SETTINGS,
            items=[
                PopupMenuItem(
                    content=Container(
                        content=self.coverSwitch
                    )
                ),
                PopupMenuItem(),
                PopupMenuItem(
                    content=Container(
                        content=self.lyricSwitch
                    )
                )
            ],
            tooltip='高级',
            disabled=True
        )
            
        self.view = Container(
            content=Column(
                controls=[
                    Row(
                        controls=[
                            Row(
                                controls=[
                                    Container(width=10), # placeholder
                                    self.selectAllCheckbox,
                                    self.numLabel,
                                    self.sizeLabel,
                                ],
                                width=270,
                                alignment='start'
                            ),
                            Row(
                                controls=[
                                    self.resFoundChip,
                                    self.noneFoundChip,
                                ],
                                width=230,
                                alignment='start'
                            ),
                            Row(
                                controls=[
                                    self.downloadButton,
                                    self.settingsButton
                                ],
                            )
                        ],
                        width=self.app.page.width-5
                    ),
                    Container(
                        content=ProgressRing(
                            width=50,
                            height=50,
                            visible=True,
                            stroke_width=3
                        ),
                        alignment=alignment.center,
                        width=self.app.page.width,
                        height=400
                    )
                ]
            ),
            width=self.app.page.width,
            height=self.app.page.height-56-5,
            margin=margin.only(top=5),
        )
        return self.view

    
    def selectAll(self, e):
        for item in self.entryList:
            if item.checkBox.disabled == False:
                item.checkBox.value = self.selectAllCheckbox.value
                item.selectFlag = self.selectAllCheckbox.value
        self.calNum(self.entryList)
        self.calSize(self.entryList)
    

    def showEntry(self, e):
        if self.resFoundChip.selected == True and self.noneFoundChip.selected == False:
            for entry in self.entryList:
                if entry.resourceState == True:
                    entry.visible = True
                else:
                    entry.visible = False
        elif self.resFoundChip.selected == False and self.noneFoundChip.selected == True:
            for entry in self.entryList:
                if entry.resourceState == False:
                    entry.visible = True
                else:
                    entry.visible = False
        elif self.resFoundChip.selected == True and self.noneFoundChip.selected == True:
            for entry in self.entryList:
                if entry.visible == False:
                    entry.visible = True
        elif self.resFoundChip.selected == False and self.noneFoundChip.selected == False:
            for entry in self.entryList:
                if entry.visible == True:
                    entry.visible = False
        self.view.update()


    def setMusicList(self, musicList: list[Music]):
        counter = count(1, 1)
        size = 0
        self.musicList = musicList
        self.entryList: list[MusicEntry] = []
        for music in self.musicList:
            tmp = MusicEntry(music, next(counter), self.select)
            if tmp.resourceState == True:
                tmp.visible = True
                size += 1
            else:
                tmp.visible = False
            self.entryList.append(tmp)
        self.listView = Container(
            content=Column(
                controls=self.entryList,
                scroll='auto',
            ),
            margin=margin.only(left=20, right=20, top=5, bottom=10),
            height=self.app.page.height-56-5-75,
            alignment=alignment.top_center
        )
        # self.showList[1].visible = False
        self.view.content.controls[-1] = self.listView
        self.selectAllCheckbox.disabled = False
        self.resFoundChip.disabled = False
        self.noneFoundChip.disabled = False
        self.settingsButton.disabled = False
        self.downloadButton.disabled = False
        self.validNum = size
        self.calNum(self.entryList)
        self.calSize(self.entryList)
        self.view.update()
    

    def select(self, idx, size, e: ControlEvent):
        self.entryList[idx-1].selectFlag = e.control.value
        self.calNum(1, e.control.value)
        self.calSize(size, e.control.value)
        self.view.update()

    
    def calNum(self, x: list[MusicEntry] | int, type: bool=True):
        if isinstance(x, list):
            num = 0
            for entry in x:
                if entry.selectFlag == True:
                    num += 1
        else:
            num = int(re.findall(r'(\d+)/', self.numLabel.value)[0])
            if type:
                num += 1
            else:
                num -= 1
        self.numLabel.value = f'{num}/{self.validNum}({self.count})'
        if num == 0:
            self.downloadButton.disabled = True
        else:
            self.downloadButton.disabled = False 
        self.view.update()


    def calSize(self, x: list[MusicEntry] | int, type: bool=True):
        if isinstance(x, list):
            size = float(0)
            for entry in x:
                if entry.selectFlag == True:
                    size += entry.music.size
        else:
            unit = self.sizeLabel.value[-2:]
            if unit == 'GB':
                size = float(self.sizeLabel.value[:-2])*1024
            elif unit == 'MB':
                size = float(self.sizeLabel.value[:-2])
            if type:
                size += x
            else:
                size -= x
        num = int(re.findall(r'(\d+)/', self.numLabel.value)[0])
        if num == 0:
            size = 0.00
        if size > 1024:
            self.sizeLabel.value = f'{size/1024:.2f}GB'
        else:
            self.sizeLabel.value = f'{size:.2f}MB'
        self.view.update()

    
    def transfer(self):
        i = 0
        for music in self.entryList:
            i += 1 if music.selectFlag else 0
        return i, self.coverSwitch.value, self.lyricSwitch.value


    def download(self, e):
        self.app.page.go('/download')
        pass