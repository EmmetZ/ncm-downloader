import re
import requests
from pyncm_async.apis.track import GetTrackLyrics
from pathlib import Path
from mutagen.id3 import (
    ID3,
    TT2,   #`标题
    TPE1,  # 作曲家
    TALB,  # 专辑名
    APIC,  # 封面
    TRCK,  # 音轨
)


class Music:
    def __init__(
        self, 
        title: str, 
        idx: int, 
        src: str,
        trackNum: int,
        size: int, 
        bitrate: int,
        encodeType: str, 
        quality: str,
        artist: list, 
        album: str, 
        picUrl: str
    ):
        self.title = title
        self.idx = idx
        self.src = src
        self.trackNum = trackNum
        self.size = size / 1024 / 1024  # 单位MB
        self.bitrate = bitrate
        self.encodeType = encodeType
        self.quality = quality
        self.artist = artist  # 作曲家
        self.album = album  # 专辑名
        self.picUrl = picUrl  # 封面链接
        self.adjustTitle()
        self.downloadFlag = False if self.src == None else True

    
    @classmethod
    def setParams(cls, savepath: Path, cover, lyric, downloadView):
        cls.basepath = savepath
        cls.coverLabel = cover
        cls.lyricLabel = lyric
        cls.downloadView = downloadView


    def adjustTitle(self):
        pattern = r"[\\/:*?\"<>|]"
        if re.search(pattern, self.title):
            self.filename = re.sub(pattern, "_", self.title)
        else:
            self.filename = self.title


    async def download(self, session):   
        savepath = self.basepath.joinpath(self.filename).with_suffix(f'.{self.encodeType}')
        if self.src == None or self.downloadFlag == False:
            return
        elif not savepath.exists():
            async with session.get(self.src) as res:
                content = await res.read()
                if res.status == requests.codes.ok:
                    f = open(savepath, 'wb')
                    f.write(content)
                    f.close()
                    self.downloadView.add(self.title, '[download] 下载成功')
                    tags = ID3(savepath)
                    tags.add(TT2(encoding=3, text=self.title))
                    tags.add(TPE1(encoding=3, text=self.artist))
                    tags.add(TALB(encoding=3, text=self.album))
                    tags.add(TRCK(encoding=3, text=str(self.trackNum)))
                    tags.save(v2_version=3)
                    return 'success'
                else:
                    self.downloadView.add(self.title, '[download] 下载失败')
                    return 'failed'
        else:
            self.downloadView.add(self.title, '[download] 已存在')
            return self


    async def writeCover(self, session):
        if self.picUrl == None:
            return
        else:
            savepath = self.basepath.joinpath(self.filename).with_suffix(f'.{self.encodeType}')
            if savepath.exists():
                async with session.get(self.picUrl) as res:
                    content = await res.read()
                    if res.status == requests.codes.ok:
                        tags = ID3(savepath)
                        tags.delall('APIC')
                        tags.add(APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=content))
                        tags.save(v2_version=3)
                        self.downloadView.add(self.title, '[cover] 写入封面成功')
                    else:
                        self.downloadView.add(self.title, '[cover] 写入封面失败')
            else:
                self.downloadView.add(self.title, '[cover] 歌曲未找到')

    
    async def downloadLyric(self):
        if self.lyricLabel == False:
            return
        else:
            res: dict = await GetTrackLyrics(self.idx)
            if res.__contains__('pureMusic'):
                if res['pureMusic'] == True:
                    self.downloadView.add(self.title, '[lyric] 纯音乐，无歌词')
                    return
            if res.__contains__('lrc'):
                if len(res['lrc']['lyric']) > 0:
                    lrcPath = self.basepath.joinpath(self.filename).with_suffix('.lrc')
                    f = open(lrcPath, 'w', encoding='utf-8')
                    f.write(res['lrc']['lyric'])
                    f.close()
            if res.__contains__('tlyric'):
                if len(res['tlyric']['lyric']) > 0:
                    tlrcPath = self.basepath.joinpath(f'{self.filename}_tlrc').with_suffix('.lrc')
                    f = open(tlrcPath, 'w', encoding='utf-8')
                    f.write(res['tlyric']['lyric'])
                    f.close()
            if res.__contains__('romalrc'):
                if len(res['romalrc']['lyric']) > 0:
                    romalrcPath = self.basepath.joinpath(f'{self.filename}_rlrc').with_suffix('.lrc')
                    f = open(romalrcPath, 'w', encoding='utf-8')
                    f.write(res['romalrc']['lyric'])
                    f.close()
            self.downloadView.add(self.title, '[lyric] 歌词下载成功')

    