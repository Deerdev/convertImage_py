#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PIL import Image as image
import os
import random
import numpy

__author__ = "Sweetfish"

H2W_ratio = 0.0
inputpath="."
b_outfilrpath = "F:\MyHomePage\\fish_source\PP\imgs-big"
s_outfilrpath = "F:\MyHomePage\\fish_source\PP\imgs-small"
maskpath = "mask"
picturePath = "raw"
blue_list_bottomleft = ['mask_blue_left.png','mask_blue_bottom.png']
blue_list_bottomright = ['mask_blue_right.png','mask_blue_bottom.png']
blue_list_topleft = ['mask_blue_left.png','mask_blue_top.png']
blue_list_topright = ['mask_blue_right.png','mask_blue_top.png']
green_list_bottomleft = ['mask_green_left.png','mask_green_bottom.png']
green_list_bottomright = ['mask_green_right.png','mask_green_bottom.png']
green_list_topleft = ['mask_green_left.png','mask_green_top.png']
green_list_topright = ['mask_green_right.png','mask_green_top.png']
#两组水印：蓝色和绿色
mask_list_blue = [blue_list_topleft,blue_list_topright,blue_list_bottomleft,blue_list_bottomright];
mask_list_green = [green_list_topleft,green_list_topright,green_list_bottomleft,green_list_bottomright];
mask_list = [mask_list_blue,mask_list_green]



#对给定图片的采样100个点计算方差
#返回方差
def computeVariance(m_im):
	img_arry = m_im.load()
	m_w,m_h = m_im.size
	pixelList=[]
	n=0

	while n <20:
		t_w = int(m_w*0.05*n)
		m = 0
		n = n+1
		while m < 9:
			t_h = int(m_h*0.1*m)
			pixelList.append(img_arry[t_w,t_h])
			m=m+1

	m_variance = numpy.var(pixelList)
	print m_variance
	return m_variance

#对给定图片的采样100个点计算G和B
#返回水印类型
def computeGB(m_im,location,location_dict,m_w,m_h):
	print "put mask on "+location
	#分割出图片
	box = (location_dict[location][0], location_dict[location][1], location_dict[location][0]+m_w, location_dict[location][1]+m_h)
	img_region = m_im.crop(box)

	img_arry = img_region.load()
	t_w,t_h = img_region.size

	pixelGList=[]
	pixelBList=[]
	pixelRList=[]
	n=0
	while n <9:
		t_w = int(m_w*0.1*n)
		m = 0
		n = n+1
		while m < 9:
			t_h = int(m_h*0.1*m)
			pixelRList.append(img_arry[t_w,t_h][0])
			pixelGList.append(img_arry[t_w,t_h][1])
			pixelBList.append(img_arry[t_w,t_h][2])
			m=m+1

	t_Rmean = numpy.mean(pixelRList)
	t_Gmean = numpy.mean(pixelGList)
	t_Bmean = numpy.mean(pixelBList)
	print "GB:"
	print (t_Gmean,t_Bmean)
	t_type = 0
	#绿色过多，用蓝色水印
	if t_Bmean > 165 and t_Gmean <165:
		t_type = 1
	elif t_Gmean > 165 and t_Bmean < 165:
		t_type = 0
	else:
		t_mean = int((t_Bmean+t_Gmean)/2)
		if t_Rmean < t_mean:
			t_type = 1
		else:
			t_type = random.randint(0,1);
			print "random_GB"
		
	return t_type

#根据水印所在的角 返回在水印数组中的下标
def getMaskType(maskLocation):
	if maskLocation == "lefttop":
		return 0
	if maskLocation == "righttop":
		return 1
	if maskLocation == "leftbottom":
		return 2
	if maskLocation == "rightbottom":
		return 3

#判断图片四个角，哪一块区域的图像(灰度值)变化最小(适合打水印)
#返回位置字符串
def getLocation(m_im,location_dict,m_w,m_h):
	#把图像转换为灰度空间
	m_im = m_im.convert("L")
	#分割出四个角图片
	box = (location_dict["lefttop"][0], location_dict["lefttop"][1], location_dict["lefttop"][0]+m_w, location_dict["lefttop"][1]+m_h)
	lefttop_region = m_im.crop(box)
	box = (location_dict["righttop"][0], location_dict["righttop"][1], location_dict["righttop"][0]+m_w, location_dict["righttop"][1]+m_h)
	righttop_region = m_im.crop(box)
	box = (location_dict["leftbottom"][0], location_dict["leftbottom"][1], location_dict["leftbottom"][0]+m_w, location_dict["leftbottom"][1]+m_h)
	leftbottom_region = m_im.crop(box)
	box = (location_dict["rightbottom"][0], location_dict["rightbottom"][1], location_dict["rightbottom"][0]+m_w, location_dict["rightbottom"][1]+m_h)
	rightbottom_region = m_im.crop(box)
	#分别计算四个角的方差
	lefttop_variance = computeVariance(lefttop_region)
	righttop_variance = computeVariance(righttop_region)
	leftbottom_variance = computeVariance(leftbottom_region)
	rightbottom_variance = computeVariance(rightbottom_region)
	#获取最小方差的位置
	t_type = "rightbottom"
	minVariance = 1000
	if minVariance > rightbottom_variance:
		minVariance = rightbottom_variance
		# t_type = "rightbottom"

	if minVariance > leftbottom_variance:
		minVariance = leftbottom_variance
		t_type = "leftbottom"

	if minVariance > righttop_variance:
		minVariance = righttop_variance
		t_type = "righttop"

	if minVariance > lefttop_variance:
		minVariance = lefttop_variance
		t_type = "lefttop"

	return t_type


#图片添加水印
#返回添加水印后的图片
def addMask(m_im):
	global mask_list_blue
	global mask_list_green
	global maskpath
	global inputpath

	#组合水印的文件夹目录mask
	t_maskpath = os.path.join(inputpath,maskpath)
	#随机获取水印类型(竖立-0，横立-1)两种
	mask_type = random.randint(0,1);
	t_imgpath = os.path.join(t_maskpath,mask_list_blue[0][mask_type])
	im_mask = image.open(t_imgpath)
	#根据类型读取水印实际大小，计算高宽比
	t_w,t_h = im_mask.size
	t_radio = float(t_h)/t_w
	b_w,b_h = m_im.size
	#按1.8%的高度读取水印离图片边界的距离
	mask_interval = int(b_h*0.018)
	
	#根据水印类型和实际图片的大小，计算出水印调整后的大小
	#具体的(百分比)都是事先在PS中计算出来的
	if mask_type==0:
		#竖立按11%高等比例缩放
		t_h = int(b_h*0.11)
		t_w = int(t_h/t_radio)
		im_mask=im_mask.resize((t_w,t_h),image.ANTIALIAS)
	else:
		#横立按7.5%高等比例缩放
		t_h = int(b_h*0.075)
		t_w = int(t_h/t_radio)
		im_mask=im_mask.resize((t_w,t_h),image.ANTIALIAS)
	
	#计算两种水印类型在实际图片上的贴图左上角位置
	maskV_location_point ={'lefttop':(0,mask_interval),'righttop':(b_w-t_w,mask_interval),'leftbottom':(0,b_h-t_h-mask_interval),\
	'rightbottom':(b_w-t_w,b_h-t_h-mask_interval)}
	maskH_location_point ={'lefttop':(mask_interval,0),'righttop':(b_w-t_w-mask_interval,0),'leftbottom':(mask_interval,b_h-t_h),\
	'rightbottom':(b_w-t_w-mask_interval,b_h-t_h)}
	mask_location = "rightbottom"
	#获取贴图位置和具体的贴图类型
	if mask_type==0:
		mask_location = getLocation(m_im,maskV_location_point,t_w,t_h)
		t_VHtype = getMaskType(mask_location)    #获取水印在四个角的位置下标
		t_RGBtype = computeGB(m_im,mask_location,maskV_location_point,t_w,t_h)    #获取水印的颜色下标
		t_imgpath = os.path.join(t_maskpath,mask_list[t_RGBtype][t_VHtype][mask_type])
		print "maskpath:"+t_imgpath
		im_mask = image.open(t_imgpath)
		im_mask = im_mask.resize((t_w,t_h),image.ANTIALIAS)
		m_im.paste(im_mask,maskV_location_point[mask_location],im_mask.convert('RGBA'))
	else:
		mask_location = getLocation(m_im,maskH_location_point,t_w,t_h)
		t_VHtype = getMaskType(mask_location)
		t_RGBtype = computeGB(m_im,mask_location,maskH_location_point,t_w,t_h)
		t_imgpath = os.path.join(t_maskpath,mask_list[t_RGBtype][t_VHtype][mask_type])
		print "maskpath:"+t_imgpath
		im_mask = image.open(t_imgpath)
		im_mask = im_mask.resize((t_w,t_h),image.ANTIALIAS)
		m_im.paste(im_mask,maskH_location_point[mask_location],im_mask.convert('RGBA'))
	return m_im

#转换成一个清晰的图片，直接保存
def saveBigPicture(b_im,b_filename,b_savepath='.'):
	global H2W_ratio
	#获取读入图片的大小，等比例缩放，宽固定为3000px
	b_w,b_h = b_im.size;
	if b_w > b_h:
		b_w = 1200;
		b_h = int(b_w*H2W_ratio);
	else:
		b_h=1200;
		b_w=int(b_h/H2W_ratio);
	b_im = b_im.resize((b_w,b_h),image.ANTIALIAS);
	#添加水印
	#b_im = addMask(b_im)
	b_filename = b_filename + "_b.jpg";
	outpath = os.path.join(b_outfilrpath, b_filename);
	b_im.save(outpath,quality=100)

#压缩转换成小画质图片，不加水印，直接保存
def saveSmallPicture(s_im,s_filename,s_savepaht= '.'):
	global H2W_ratio
	s_height = int(200 * H2W_ratio);    #等比例缩放，固定宽为1000px
	s_im = s_im.resize((200,s_height),image.ANTIALIAS);
	s_filename = s_filename + "_s.jpg";
	outpath = os.path.join(s_outfilrpath,s_filename);
	s_im.save(outpath,quality=100);

#读入图片，转换出一个预览图和一个稍清晰的图片
def convertImage(fpath):
	global H2W_ratio
	im = image.open(fpath)
	#分离文件夹路径+文件名.jpg
	filename_attri = os.path.split(fpath);
	#分离文件名和后缀
	filename_arry = os.path.splitext(filename_attri[1])
	filename = filename_arry[0]
	ori_width,ori_height = im.size
	H2W_ratio = float(ori_height)/ori_width

	saveSmallPicture(im,filename);
	saveBigPicture(im,filename);
	

#遍历输入文件夹下的jpg类型图片，进行图片转换
def readDirPath(dirPath):
	#组合图片的源目录pic文件夹
	imgpath = os.path.join(dirPath,picturePath)
	images = []
	for x in os.listdir(imgpath):
		fpath = os.path.join(imgpath,x)
		if os.path.isfile(fpath):
			if fpath.find('jpg')!= -1:
				images.append(fpath)
	# print images
	images_size = len(images)
	curent_i = 1;
	for x in images:
		convertImage(x)
		print x
		print "(%d/%d)finished!" % (curent_i,images_size)
		print "**************************************************"
		curent_i += 1

#调用函数
readDirPath(inputpath);