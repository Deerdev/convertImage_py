from PIL import Image as image
import datetime
import os
import random

im = image.open("./3.jpg")
im=im.convert("L")
m_w,m_h = im.size
stat = datetime.datetime.now()
im_arry = im.load()
print im_arry[0,0]
print im_arry[100,100]
end = datetime.datetime.now()
#print (end-stat).seconds