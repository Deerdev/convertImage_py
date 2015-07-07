#-*- coding: utf-8 -*-

import os

htmlfilepath = './allimage.html'
DIR = './pic2'

#倒序
def compare(x,y):
    if x > y:
        return -1
    elif x<y:
        return 1
    else:
        return 0

def read2html(iterm,fd):
    fd.write(r'<div class="box_imgs">')
    fd.write(r'<div class="box_img">')
    i = int(iterm)
    alink = r'<a class="fancybox" href="http://7xijgf.com1.z0.glb.clouddn.com/image-big/%d_b.jpg">' % i
    imagelink = r'<img src="http://7xijgf.com1.z0.glb.clouddn.com/image-small/%d_s.jpg" alt="photo">' % i
    fd.write(alink)
    fd.write(imagelink)
    fd.write(r'</a></div></div>')

#读取当前文件夹下文件到list
iterms = os.listdir(DIR)
namelist=[]
for iterm in iterms:
    print iterm
    #分离文件名和后缀
    filename_arry = os.path.splitext(iterm)
    print filename_arry
    filename = filename_arry[0]
    i=int(filename)
    namelist.append(i)

print "******************************"
#按创建时间排序
namelist.sort(compare)

fd=open(htmlfilepath,'w')
fd.write(r'<div id="image_container">')
for iterm in namelist:
    read2html(iterm,fd)
fd.write(r'</div>')
fd.close()