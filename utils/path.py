from pathlib import Path
import sys

BASE = Path(__file__).parent.parent.resolve()
FONT_PATH = BASE.joinpath('assets', 'msyh.ttc')

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):  # 判断是否是打包后的exe文件在运行
    BASE_FILEPATH = BASE.parent.resolve()   # 如果是就多一层跳出_internal文件夹()
else:
    BASE_FILEPATH = BASE
 