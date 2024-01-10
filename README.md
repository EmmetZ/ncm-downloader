# ncm-downloader

一个简易网易云音乐下载脚本，支持下载单曲、歌单、专辑

API：[pyncm](https://github.com/mos9527/pyncm)

简易ui：[flet](https://flet.dev/)

⚠️**注：本脚本无法下载VIP歌曲，收听VIP歌曲请支持官方正版！！！**

## 特点

1. 支持下载单曲、歌单、专辑

2. 登陆功能，可获取完整个人歌单

3. 可自行选择要下载的歌曲，已有歌曲不会重复下载

4. 自动写入歌曲信息（歌名、歌手、专辑等）

5. 写入专辑封面（可选），下载歌词（可选）

6. 自定义保存文件夹位置

## 使用方法

release中下载已打包好的exe文件

**打包：**
使用pyinstaller打包，命令如下：

```shell
pip install pyinstaller
cd ncm-downloader
pyinstaller main.spec
```

## 致谢

感谢网易云第三方开源API：[pyncm](https://github.com/mos9527/pyncm)

网易云音乐：[https://music.163.com/](https://music.163.com/)

感谢其他所有python开源库的贡献者

