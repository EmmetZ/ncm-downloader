from pyncm.apis import playlist as pl
from pyncm.apis import album as al
from pyncm.apis.track import GetTrackAudio, GetTrackDetail
from pyncm.apis.login import (
    LoginViaAnonymousAccount,
    LoginQrcodeCheck,
    LoginQrcodeUnikey,
    GetCurrentLoginStatus,
    WriteLoginInfo
)
from pyncm import CreateNewSession, Session
from aiohttp import ClientSession
import qrcode
import re
from time import sleep, time
from pathlib import Path
import asyncio
from PIL.Image import Image
import base64
from io import BytesIO
from utils.music import Music
from utils.path import BASE_FILEPATH
import asyncio


async def asycnDownload(l: list[Music], headers: dict, f):
    if f != 'lyric':
        session = ClientSession(headers=headers)
        if f == 'download':
            tasks = [item.download(session) for item in l]
        elif f == 'cover':
            tasks = [item.writeCover(session) for item in l]
    else:
        tasks = [item.downloadLyric() for item in l]
    await asyncio.gather(*tasks)


class Clinet:
    def __init__(self) -> None:
        self.session: Session = CreateNewSession()
        self.savepath = BASE_FILEPATH
        self.coverFlag = False
        self.lyricFlag = False
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76'
        }


    def search(self, label, id) -> tuple[str]:
        match label:
            case 'playlist':
                self.label = label
                label = '歌单'
                with self.session:
                    playlist: dict = pl.GetPlaylistInfo(id)
                # with open('./test/playlist.json', 'r', encoding='utf-8') as f:
                #     playlist = json.load(f)
                if playlist['code'] != 200:
                    return 'error', '未找到资源或无访问权限'
                objName = playlist['playlist']['name']
                self.objName = objName
                self.count = playlist['playlist']['trackCount']
                self.tracks = playlist['playlist']['tracks']
            case 'album':
                self.label = label
                label = '专辑' 
                with self.session:
                    album: dict = al.GetAlbumInfo(id)
                if album['code'] == 200 and album['resourceState'] == True:
                    objName = album['album']['name']
                    self.objName = objName
                    self.count = album['album']['size']
                    self.tracks = album['songs']
                else:
                    return '未找到资源', '请登录后重试或检查链接是否正确'
            case 'song':
                self.label = label
                label = '单曲'
                with self.session:
                    song: dict = GetTrackDetail([id])
                if song['code'] != 200 or len(song['songs']) == 0:
                    return '未找到资源', '请登录后重试或检查链接是否正确'
                objName = song['songs'][0]['name']
                self.objName = objName
                self.count = 1
                self.tracks = song['songs']
            case _:
                label = '未找到'
                objName = 'error'
        return label, objName

    
    def getMusicList(self):
        self.musicList: list[Music] =[]
        idList = []
        for music in self.tracks:
            idList.append(music['id'])
        with self.session:
            tmp: list =  GetTrackAudio(idList)['data']
        # with open('./test/tracks.json', 'r', encoding='utf-8') as f:
        #     tmp = json.load(f)['data']
        musicDict = {}
        for item in tmp:
            musicDict[item['id']] = item
        for i, id in enumerate(idList):
            music = musicDict[id]
            self.musicList.append(
                Music(
                    title=self.tracks[i]['name'],
                    idx=music['id'],
                    src=music['url'],
                    size=music['size'],
                    trackNum=self.tracks[i]['no'],
                    bitrate=music['br'],
                    encodeType=music['encodeType'],
                    quality=music['level'],
                    artist=[ar['name'] for ar in self.tracks[i]['ar']],
                    album=self.tracks[i]['al']['name'],
                    picUrl=self.tracks[i]['al']['picUrl']
                )
            ) 
            del musicDict[id]


    def anonymousLogin(self) -> dict:
        with self.session:
            LoginViaAnonymousAccount()
            return GetCurrentLoginStatus()

    
    def getQrcode(self):
        with self.session:
            self.uuid = LoginQrcodeUnikey()['unikey']
            url = f'https://music.163.com/login?codekey={self.uuid}'
            img: Image = qrcode.make(url)
            tmp = BytesIO()
            img.save(tmp, format='jpeg')
            base64Img = base64.b64encode(tmp.getvalue()).decode('utf-8')
            return base64Img
    

    def loginCheck(self) -> dict:
        t = time()
        with self.session:
            while True:
                rsp = LoginQrcodeCheck(self.uuid)
                if rsp['code'] == 803 or rsp['code'] == 800:
                    WriteLoginInfo(GetCurrentLoginStatus())
                    break
                sleep(1)
                if time() - t > 30:
                    return {'code': 500, 'account': None}
            return GetCurrentLoginStatus()


    def download(self, num):
        i = 0
        tasks = []
        flag = False
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        for item in self.musicList:
            if item.downloadFlag:
                i += 1
                tasks.append(item)
            if i % 10 == 0 or i == num:
                if i == num:
                    flag = True
                # asyncio.get_event_loop().run_until_complete(asycnDownload(tasks, self.headers, 'download'))
                loop.run_until_complete(asycnDownload(tasks, self.headers, 'download'))
                if self.coverFlag:
                    loop.run_until_complete(asycnDownload(tasks, self.headers, 'cover'))
                if self.lyricFlag:
                    loop.run_until_complete(asycnDownload(tasks, self.headers, 'lyric'))
                tasks = []
            if flag:
                break
        print('download success')
    

    def setPath(self):
        if self.label != 'song':
            pattern = r"[\\/:*?\"<>|]"
            if re.search(pattern, self.objName):
                folder = re.sub(pattern, "_", self.objName)
            else:
                folder = self.objName
            self.savepath = self.savepath.joinpath(folder)
        if self.label != 'song' and not self.savepath.exists():
            self.savepath.mkdir()


    @property
    def savepath(self):
        return self._savepath

    @savepath.setter
    def savepath(self, path):
        self._savepath = Path(path)
