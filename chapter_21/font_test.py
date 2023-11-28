import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc

# data = np.random.randint(-100, 100, 50).cumsum()

# plt.plot(range(50), data, "r")
# mpl.rcParams["axes.unicode_minus"] = False
# plt.title("시간별 가격 추이")
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


path = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
fontprop = fm.FontProperties(fname=path, size=18)
plt.ylabel("세로축", fontproperties=fontprop)
plt.title("가로축", fontproperties=fontprop)
plt.show()
