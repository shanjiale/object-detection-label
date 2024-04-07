import os
import xml.etree.ElementTree as ET
import math
import cv2 as cv


def voc_to_dota(xml_path, xml_name):
    txt_name = xml_name[:-4] + '.txt'
    txt_path = xml_path + '/txt_label'
    if not os.path.exists(txt_path):
        os.makedirs(txt_path)
    txt_file = os.path.join(txt_path, txt_name)
    file_path = os.path.join(xml_path, file_list[i])
    tree = ET.parse(os.path.join(file_path))
    root = tree.getroot()
    # print(root[6][0].text)
    image_path = 'H:\\C02GF-2data\\裁剪之后的图\\GF2_PMS1_E4.0_N52.1_20210502\\images\\'
    out_path = 'H:\\C02GF-2data\\裁剪之后的图\\GF2_PMS1_E4.0_N52.1_20210502\\out\\'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    filename = image_path + xml_name[:-4] + '.jpg'
    img = cv.imread(filename)
    with open(txt_file, "w+", encoding='UTF-8') as out_file:
        # out_file.write('imagesource:null' + '\n' + 'gsd:null' + '\n')
        for obj in root.findall('object'):
            name = obj.find('name').text
            difficult = obj.find('difficult').text
            # print(name, difficult)
            robndbox = obj.find('robndbox')
            cx = float(robndbox.find('cx').text)
            cy = float(robndbox.find('cy').text)
            w = float(robndbox.find('w').text)
            h = float(robndbox.find('h').text)
            angle = float(robndbox.find('angle').text)
            # print(cx, cy, w, h, angle)
            p0x, p0y = rotatePoint(cx, cy, cx - w / 2, cy - h / 2, -angle)
            p1x, p1y = rotatePoint(cx, cy, cx + w / 2, cy - h / 2, -angle)
            p2x, p2y = rotatePoint(cx, cy, cx + w / 2, cy + h / 2, -angle)
            p3x, p3y = rotatePoint(cx, cy, cx - w / 2, cy + h / 2, -angle)

            # 找最左上角的点
            dict = {p0y:p0x, p1y:p1x, p2y:p2x, p3y:p3x }
            list = find_topLeftPopint(dict)
            #print((list))
            if list[0] == p0x:
                list_xy = [p0x, p0y, p1x, p1y, p2x, p2y, p3x, p3y]
            elif list[0] == p1x:
                list_xy = [p1x, p1y, p2x, p2y, p3x, p3y, p0x, p0y]
            elif list[0] == p2x:
                list_xy = [p2x, p2y, p3x, p3y, p0x, p0y, p1x, p1y]
            else:
                list_xy = [p3x, p3y, p0x, p0y, p1x, p1y, p2x, p2y]

            # 在原图上画矩形 看是否转换正确
            cv.line(img, (int(list_xy[0]), int(list_xy[1])), (int(list_xy[2]), int(list_xy[3])), color=(255, 255, 0), thickness= 3)
            cv.line(img, (int(list_xy[2]), int(list_xy[3])), (int(list_xy[4]), int(list_xy[5])), color=(255, 255, 0), thickness= 3)
            cv.line(img, (int(list_xy[4]), int(list_xy[5])), (int(list_xy[6]), int(list_xy[7])), color=(255, 255, 0), thickness= 2)
            cv.line(img, (int(list_xy[6]), int(list_xy[7])), (int(list_xy[0]), int(list_xy[1])), color=(255, 255, 0), thickness= 2)

            data = str(list_xy[0]) + " " + str(list_xy[1]) + " " + str(list_xy[2]) + " " + str(list_xy[3]) + " " + \
                   str(list_xy[4]) + " " + str(list_xy[5]) + " " + str(list_xy[6]) + " " + str(list_xy[7]) + " "
            data = data + name + " " + difficult + "\n"
            out_file.write(data)
            # cv.imwrite(out_path + xml_name[:-4] + '.jpg', img)  # 可能CV版本与环境不兼容，不显示图片即可


def find_topLeftPopint(dict):
    dict_keys = sorted(dict.keys())  # y值
    temp = [dict[dict_keys[0]], dict[dict_keys[1]]]
    minx = min(temp)
    if minx == temp[0]:
        miny = dict_keys[0]
    else:
        miny = dict_keys[1]
    return [minx, miny]


# 转换成四点坐标
def rotatePoint(xc, yc, xp, yp, theta):
    xoff = xp - xc
    yoff = yp - yc
    cosTheta = math.cos(theta)
    sinTheta = math.sin(theta)
    pResx = cosTheta * xoff + sinTheta * yoff
    pResy = - sinTheta * xoff + cosTheta * yoff
    # pRes = (xc + pResx, yc + pResy)
    # 保留一位小数点
    return float(format(xc + pResx, '.1f')), float(format(yc + pResy, '.1f'))
    # return xc + pResx, yc + pResy


if __name__ == '__main__':
    root_path = 'H:\\飞机数据\\标签\\1'
    file_list = os.listdir(root_path)
    for i in range(0, len(file_list)):
        if ('.xml' in file_list[i]) or ('.XML' in file_list[i]):
            voc_to_dota(root_path, file_list[i])
            print('----------------------------------------{}{}----------------------------------------'
                  .format(file_list[i], ' has Done!'))
        else:
            print(file_list[i] + ' is not xml file')
