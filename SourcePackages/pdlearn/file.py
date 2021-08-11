import os
import sys
import json
from pyhocon import ConfigFactory

def check_directory(filename):
    # filename 最多支持一层文件夹下的json
    # os.chdir(sys.path[0]) # 切换pwd到python文件路径
    split_filename = filename.split("/", 1)
    if(len(split_filename) > 1): # 包含一层文件夹
        if(not os.path.exists(split_filename[0])):
            os.mkdir(split_filename[0])

def get_json_data(filename, template_json_str):
    check_directory(filename)
    if(os.path.exists(filename) and os.path.getsize(filename) != 0):
        with open(filename, 'r', encoding = 'utf-8') as j:
            try:
                json_data = json.load(j)
            except Exception as e:
                print(filename, "解析错误：", str(e))
                print("请检查", filename, "信息")
                exit()
    else:
        json_data = json.loads(template_json_str)
    return json_data

def save_json_data(filename, object_to_save, sort_keys=True):
    check_directory(filename)
    with open(filename,'w', encoding = 'utf-8') as o:
        json.dump(object_to_save, o, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)


def get_conf_file(filename, template_conf_str):
    check_directory(filename)
    if(os.path.exists(filename) and os.path.getsize(filename) != 0):
        try:
            conf_obj = ConfigFactory.parse_file(filename)
        except Exception as e:
            print(filename, "解析错误：", str(e))
            print("请检查", filename, "信息")
            exit()
    else:
        save_text_file(filename, template_conf_str)
        conf_obj = get_conf_file(filename, template_conf_str)
    return conf_obj


def save_text_file(filename, text):
    check_directory(filename)
    with open(filename,'w', encoding = 'utf-8') as o:
        o.write(text)
