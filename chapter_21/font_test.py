# https://python-graph-gallery.com/custom-fonts-in-matplotlib/
# https://gree2.github.io/python/2015/04/27/python-change-matplotlib-font-on-mac
import pathlib

import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

# rc("font", family="Apple SD Gothic Neo")  ## 이 두 줄을

FONT_PATH = pathlib.Path(__file__).parent.parent / "font/Pretendard-Bold.ttf"
font_name = fm.FontProperties(fname=FONT_PATH).get_name()
rc("font", family=font_name)  ## 이 두 줄을


path = "C:\\Users\\Downloads\\NanumBarunGothic.ttf"
fontprop = fm.FontProperties(fname=path, size=18)
plt.ylabel("세로축", fontproperties=fontprop)
plt.title("가로축", fontproperties=fontprop)
plt.show()
# 출처: https://wotres.tistory.com/entry/pyplot-에서-한글-깨짐-문제-해결법 [Carl's Tech Blog:티스토리]

# rc('font', family=font_name)


# remove mpl cache
sorted(fm.fontManager.get_font_names())
sorted([font.name for font in fm.fontManager.ttflist])
print("버전: ", mpl.__version__)
print("설치 위치: ", mpl.__file__)
print("설정 위치: ", mpl.get_configdir())
print("캐시 위치: ", mpl.get_cachedir())
print("설정파일 위치: ", mpl.matplotlib_fname())

sorted(fm.findSystemFonts())
# sorted(fm.findSystemFonts(fontpaths=None, fontext="ttf"))
# font_prop = fm.FontProperties(fname="/Library/Fonts/NanumGothic.otf")
# font_prop.get_name()
# rc("font", family=font_prop.get_name())  ## 이 두 줄을
# rc("font", family="Apple SD Gothic Neo")  ## 이 두 줄을

# FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()


# runtime configuration params
# https://matplotlib.org/stable/users/explain/customizing.html
# https://jrc-park.tistory.com/274
mpl.rcParams
mpl.rcParams["axes.edgecolor"] = "red"
mpl.rcParams["axes.facecolor"] = "yellow"
# plt.plot([1, 3, 2])
# plt.title("한글🥰")
# plt.xlabel("가로축")
# plt.ylabel("세로축")
# plt.show()

plt.plot([1, 3, 2], [-1, 0, 1])
# plt.title("한글🥰", fontdict=dict(family="AppleSDGothic"))
# plt.title("한글🥰", fontdict=dict(family="/Library/Fonts/NanumGothic.otf"))
plt.title("한글", font=FONT_PATH)
# plt.xlabel("가로축", fontdict={})
plt.ylabel("세로축", font=FONT_PATH)
plt.show()


# data = np.random.randint(-100, 100, 50).cumsum()

# plt.plot(range(50), data, "r")
# mpl.rcParams["axes.unicode_minus"] = False
# plt.title("시간별 가격 추이")``
# plt.ylabel("주식 가격")
# plt.xlabel("시간(분)")

# print("버전: ", mpl.__version__)
# print("설치 위치: ", mpl.__file__)
# print("설정 위치: ", mpl.get_configdir())
# print("캐시 위치: ", mpl.get_cachedir())

# print("설정파일 위치: ", mpl.matplotlib_fname())

# font_list = fm.findSystemFonts(fontpaths=None, fontext="ttf")
# font_list

# # ttf 폰트 전체갯수
# print(len(font_list))


# path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
# fontprop = fm.FontProperties(fname=path, size=18)
# plt.ylabel("세로축", fontproperties=fontprop)
# plt.title("가로축", fontproperties=fontprop)
# plt.show()
