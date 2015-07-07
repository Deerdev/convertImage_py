#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import exifread
import time
import datetime
import types

DIR = "./pic"
newDIR = "./pic2"

#读取照片的拍摄时间，没有就读取创建时间
def getCreatTime(filepath):
	try:
		fd = open(filepath,'rb')
	except:
		raise "can't open file[%s]\n" % filepath
	info = exifread.process_file(fd)
	fd.close()
	if info:
		try:
			#EXIF.py xx.jpg ---读取图片exif信息，查看输出的dict数据，取拍摄时间数据
			creat_time=info['EXIF DateTimeOriginal']
			#creat_time不是str，需要转换
			creat_time_ss = str(creat_time)
			#字符串格式2015:05:03 19:40:23  转为毫秒格式输出
			creat_time_date = datetime.datetime.strptime(creat_time_ss,"%Y:%m:%d %H:%M:%S")
			creat_time_float = time.mktime(creat_time_date.timetuple())
			#print int(creat_time_float)
			return int(creat_time_float)
		except:
			pass
	#读取创建时间
	newtime = os.stat(filepath)
	creat_time_ct = newtime.st_ctime
	return int(creat_time_ct)

#比较两个照片文件的创建时间，按由早到晚排列
def compare(x,y):
	stat_x =getCreatTime(os.path.join(DIR,x))
	stat_y = getCreatTime(os.path.join(DIR,y))
	if stat_x< stat_y:
		return -1
	elif stat_x > stat_y:
		return 1
	else:
		return 0

#读取当前文件夹下文件到list
iterms = os.listdir(DIR)
# for iterm in iterms:
# 	print iterm
print "******************************"
#按创建时间排序
iterms.sort(compare)

#重命名，从1.jpg开始叠加
i = 1
for iterm in iterms:
	newName = str(i) + '.jpg'
	os.rename(os.path.join(DIR,iterm),os.path.join(newDIR,newName))
	i = i+1