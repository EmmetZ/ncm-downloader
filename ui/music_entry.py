from flet import (
    Text,
    colors,
    Container,
    Row,
    margin,
    padding,
    border_radius,
    Checkbox,
    border,
    MainAxisAlignment,
    alignment,
)
from utils.music import Music
from functools import partial


class MusicEntry(Row):
    def __init__(self, music: Music, idx, func):
        super().__init__()
        self.music: Music = music
        if self.music.src != None:
            self.resourceState = True
        else:
            self.resourceState = False
        self.idx = idx
        self.selectFlag = self.resourceState and self.music.downloadFlag
        self.build(func)


    def build(self, func):
        if self.resourceState:
            self.musicName = Text(
                value=f'{self.idx}. {self.music.title}',
                color=colors.BLACK
            )
            self.size = Container(
                content=Text(
                    value='{:.2f}MB'.format(self.music.size),
                    color=colors.BLACK
                ),
                margin=margin.all(0),
                bgcolor=colors.RED_100,
                padding=padding.all(5),
                border_radius=border_radius.all(5)
            )
            self.encodeType = Container(
                content=Text(
                    value=self.music.encodeType,
                    color=colors.BLACK
                ),
                margin=margin.all(0),
                padding=padding.all(5),
                bgcolor=colors.RED_100,
                border_radius=border_radius.all(5)
            )
            self.quality = Container(
                content=Text(
                    value=self.music.quality,
                    color=colors.BLACK
                ),
                margin=margin.all(0),
                padding=padding.all(5),
                bgcolor=colors.RED_100,
                border_radius=border_radius.all(5)
            )
        else:
            self.musicName = Text(
                value=f'{self.idx}. {self.music.title}',
                color=colors.GREY
            )
        self.checkBox = Checkbox(
            value=self.selectFlag,
            disabled=not self.resourceState,
            on_change=partial(func, self.idx, self.music.size)
        )
        self.view = Container(
            content=Row(
                controls=[
                    Row(
                        controls=[
                            self.checkBox,
                            self.musicName
                        ],
                        width=400,
                    ),
                    Row(
                        controls=[
                            self.encodeType if self.resourceState else Container(),
                            self.quality if self.resourceState else Container(),
                            self.size if self.resourceState else Container(),
                        ]
                    ),
                ],
            ),
            width=620,
            margin=margin.all(0),
            border_radius=border_radius.all(10),
            border=border.all(1, colors.RED_300),
            alignment=alignment.center
        )
        self.controls = [self.view]
        self.alignment = MainAxisAlignment.CENTER
        self.width = 650


    # @property
    # def resourceState(self):
    #     return self._resourceState
    
    # @resourceState.setter
    # def resourceState(self, value):
    #     self._resourceState = value