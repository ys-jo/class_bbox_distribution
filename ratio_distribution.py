"""
made by : ys-jo
date : 22.08

Input
- PASCAL VOC xml format file or dir

Results
- class distribution
- bbox size distribution
"""


import os
import argparse
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
from tqdm import tqdm


def args():
    parser = argparse.ArgumentParser(description="ratio distribution")
    parser.add_argument('--input', type=str, help='input xml directory path or xml file', required=True)
    parser.add_argument('--output', type=str, help='output dir', required=True)
    args = parser.parse_args()
    return args


def read_xml(data_xml):
    final_data = list()
    print("read xml file")
    for data in tqdm(data_xml):
        check = 0
        tree = ET.parse(data)
        size = tree.find("size")
        width = size.find("width").text
        height = size.find("height").text

        objects = tree.findall("object")
        for i, obj in enumerate(objects):
            s_data = list()
            name = obj.find("name").text

            bndbox = obj.find("bndbox")
            bnd_width = (float(bndbox.find('xmax').text) - float(bndbox.find('xmin').text))/float(width)
            bnd_height = (float(bndbox.find('ymax').text) - float(bndbox.find('ymin').text))/float(height)
            if bnd_width > 1 or bnd_height > 1:
                check = 1
            if check == 0:

                s_data.append(name)
                s_data.append(round(bnd_width,3))
                s_data.append(round(bnd_height,3))

                final_data.append(s_data)
        if check == 1:
            print("remove")
            os.remove(data)
    """
    findal data structure
    [[class_name, width, height].[class_name, width, height],[class_name, width, height],...]
    """
    return final_data


def make_dir(dir):
    if not os.path.isdir(dir):
        print("make output dir")
        os.mkdir(dir)

def check_input(arg):
    """
    check dir or file
    ret : list(path)
    """
    data_xml = list()

    if os.path.isfile(arg.input) and arg.input[-3:] == 'xml':
        data_xml.append(arg.input)
        return data_xml
    elif os.path.isdir(arg.input):
        if not arg.input[-1] == '/':
            arg.input = arg.input +'/'
        file_list = os.listdir(arg.input)
        for file in file_list:
            if file[-3:] == 'xml':
                data_xml.append(arg.input + file)
        if data_xml:
            return data_xml
        else:
            raise Exception("Input arg is wrong")
    else:
        raise Exception("Input arg is wrong")
         

def classifier(data):
    #class distribution
    print("class data")
    class_data = dict()
    for d in tqdm(data):
        if not d[0] in class_data:
            class_data[d[0]] = 1
        else:
            class_data[d[0]] += 1
    
    #bbox ratio distribtuion
    print("size_data")
    width = list()
    height = list()
    for i in tqdm(data):
        width.append(i[1])
        height.append(i[2])

    return class_data, width, height


def plot(class_data, width_data, height_data, output):

    item = class_data.items()
    x,y = zip(*item)
    plt.subplot(2, 1, 1)
    plt.plot(x,y)
    plt.xlabel('class')
    plt.ylabel('num')
    plt.title("class distribution")
    plt.xticks(rotation=45)
    plt.grid(True)


    plt.subplot(2,1,2)
    plt.scatter(width_data, height_data, s=1)
    plt.grid(True)
    plt.xlabel('width')
    plt.ylabel('height')
    plt.title("size distribution")
    plt.tight_layout()
    plt.savefig(output+'/result.png', dpi=300)
    plt.show()



def main(arg):
    data_xml = check_input(arg)
    data = read_xml(data_xml)
    make_dir(arg.output)
    class_data, width_data, height_data = classifier(data)
    plot(class_data, width_data, height_data, arg.output)


if __name__ == "__main__":
    arg = args()
    main(arg)