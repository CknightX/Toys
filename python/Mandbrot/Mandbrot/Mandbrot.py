import time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from mpmath import *
import colorsys
import math
# 绘制图片尺寸
height=480
width=640
# 配色方案
MAXCOLOR=64
color=[(0,0,0) for i in range(MAXCOLOR)]
color_inited=False
# 默认迭代最大次数
DEFAULT_ITER_MAX=200
# 默认虚数空间
DEFAULT_IMAG_TL=(mpf(-2.1),mpf(-1.2))  # top left
DEFAULT_IMAG_BR=(mpf(1.1),mpf(1.2))    # bottom right

def coord_map(point_real,imag_top_left,imag_lower_right):
	"""坐标映射，屏幕空间->虚数空间,注意屏幕空间坐标系xy和虚数空间相反
	point_real:       (float,float) 实数空间坐标
	imag_top_left:    (float,float) 虚数空间左上角
	imag_lower_right: (float,float) 虚数空间右下角
	return:           complex       虚数
	"""
	c_real=imag_top_left[0]+(imag_lower_right[0]-imag_top_left[0])*(point_real[1]/width)
	c_imag=imag_top_left[1]+(imag_lower_right[1]-imag_top_left[1])*(point_real[0]/height)
	return (c_real,c_imag)

def point_iter_count(point_imag,iter_max_limit):
	""""迭代次数计算
	point_imag: (float,float) 虚数空间坐标
	return:     int           >0  发散点的迭代次数
				int			  ==0 收敛点
	"""
	c=complex(point_imag[0],point_imag[1])
	z=complex(0,0)
	for m in range(iter_max_limit):
		z=z*z+c
		if z.real*z.real + z.imag*z.imag>4:
			return m
	return 0

def hls_to_rgb(h,s,l):
	"""hls转rgb"""
	if s > 0:
		v_1_3 = 1.0 / 3
		v_1_6 = 1.0 / 6
		v_2_3 = 2.0 / 3
		q = l * (1 + s) if l < 0.5 else l + s - (l * s)
		p = l * 2 - q
		hk = h / 360.0 # h 规范化到值域 [0, 1) 内
		tr = hk + v_1_3
		tg = hk
		tb = hk - v_1_3
		rgb = [
			tc + 1.0 if tc < 0 else
			tc - 1.0 if tc > 1 else
			tc
			for tc in (tr, tg, tb)
			]
		rgb = [
			p + ((q - p) * 6 * tc) if tc < v_1_6 else
			q if v_1_6 <= tc < 0.5 else
			p + ((q - p) * 6 * (v_2_3 - tc)) if 0.5 <= tc < v_2_3 else
			p
			for tc in rgb
			]
		rgb = tuple(int(i * 255) for i in rgb)
	# s == 0 的情况
	else:
		rgb = l, l, l
	return rgb
def init_color():
	"""生成配色"""
	global color
	h1=240
	h2=30
	for i in range(MAXCOLOR//2):
		color[i]=hls_to_rgb(float(h1),1.0,i*2.0/MAXCOLOR)
		color[MAXCOLOR-1-i]=hls_to_rgb(float(h2),1.0,i*2.0/MAXCOLOR)
def _draw(imag_top_left,imag_lower_right,iter_max_limit):
	"""将指定区域的虚数空间投射到(width,height)大小的区域
	imag_top_left:    虚数空间左上角坐标
	imag_lower_right: 虚数空间右下角坐标
	return:           np.array 图片数据
	"""
	_img=Image.new('RGB',(width,height))
	img=np.array(_img)
	st=set()
	for px in range(height):
		for py in range(width):
			imag_point=coord_map((px,py),imag_top_left,imag_lower_right)
			iter_count=point_iter_count(imag_point,iter_max_limit)
			if iter_count: # 发散
				for i in range(3):
					img[px,py,i]=color[iter_count%MAXCOLOR][i]
			else:
				img[px,py,:]=0
	return img
def draw(point_real,zoom,max_iter=DEFAULT_ITER_MAX):
	global color_inited
	if color_inited == False:
		init_color()
		color_inited=True
	x,y=point_real
	pl=(x-0.5*((1/mpf(zoom))**0.5)*height,y-0.5*((1/mpf(zoom))**0.5)*width)
	pr=(x+0.5*((1/mpf(zoom))**0.5)*height,y+0.5*((1/mpf(zoom))**0.5)*width)
	imag_pl=coord_map(pl,DEFAULT_IMAG_TL,DEFAULT_IMAG_BR)
	imag_pr=coord_map(pr,DEFAULT_IMAG_TL,DEFAULT_IMAG_BR)
	return _draw(imag_pl,imag_pr,max_iter)

if __name__=='__main__':
	init_color()
	# img=_draw(DEFAULT_IMAG_TL,DEFAULT_IMAG_BR,DEFAULT_ITER_MAX)
	img=draw((121,340),10)
	im=Image.fromarray(img)
	im.save('1.jpg')
	plt.imshow(img)
	plt.show()
