#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
from lxml.etree import Element, SubElement, tostring, ElementTree
from tqdm import tqdm
import xml.etree.ElementTree as ET
import pickle
import os
import numpy as np
import cv2
from os import listdir, getcwd
from os.path import join

classes = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A15",
           "A16", "A17", "A18", "A19", "A20"]  # 类别

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def convert_annotation(xmls_path, txts_path, xml_name):
    xml_path = os.path.join(xmls_path, xml_name)
    in_file = open(xml_path, encoding="UTF-8")
    txt_path = os.path.join(txts_path,xml_name).split('.xml')[0] + '.txt'
    # txt_path = xml_path.split('.xml')[0] + '.txt'



    # in_file = open('./label_xml\%s.xml' % (image_id), encoding='UTF-8')
    #
    # out_file = open('./label_txt\%s.txt' % (image_id), 'w')  # 生成txt格式文件
    tree = ET.parse(in_file)
    root = tree.getroot()

    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    if width == 0 or height == 0:
        print("%s文件中width和height为0" % xml_name)
    for obj in root.iter('object'):
        cls = obj.find('name').text
        # print(cls)
        # if cls not in classes:
        #     continue
        cls_id = classes.index(cls)
        # cls_id = 0
        xmlbox = obj.find('robndbox')
        b = ((float(xmlbox.find('x_left_top').text), float(xmlbox.find('y_left_top').text)),
             (float(xmlbox.find('x_right_top').text),float(xmlbox.find('y_right_top').text)),
             (float(xmlbox.find('x_left_bottom').text),float(xmlbox.find('y_left_bottom').text)),
             (float(xmlbox.find('x_right_bottom').text),float(xmlbox.find('y_right_bottom').text))
             )
        poly = np.float32(np.array(b))
        # 四点坐标归一化
        poly[:, 0] = poly[:, 0] / width
        poly[:, 1] = poly[:, 1] / height

        rect = cv2.minAreaRect(poly)  # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）

        c_x = rect[0][0]
        c_y = rect[0][1]
        w = rect[1][0]
        h = rect[1][1]
        if w < h:
            w, h = h, w
            the = int(int(rect[-1]) + 90) % 180
        else:
            the = (int(rect[-1]) + 180)
        with open(txt_path, 'a', encoding="UTF-8") as out_file:  # 生成yolo的txt格式文件
            out_file.write('%s %s %s %s %s %s\n' % (cls_id, c_x, c_y, w, h, the))


# xml_path = os.path.join(CURRENT_DIR, './label_xml/')
xmls_path = r"H:\飞机数据\MAR20\Annotations\Oriented Bounding Boxes"
txts_path = r"H:\飞机数据\MAR20\Annotations\txt"

# xml list
img_xmls = os.listdir(xmls_path)

for img_xml in tqdm(img_xmls):
    #label_name = img_xml.split('.')[0]
    #print(label_name)
    convert_annotation(xmls_path,txts_path, img_xml)

