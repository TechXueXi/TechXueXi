import os
import sys
import json
from pyhocon import ConfigFactory


def check_directory(filename):
    # filename 最多支持一层文件夹下的json
    # os.chdir(sys.path[0]) # 切换pwd到python文件路径
    split_filename = filename.split("/", 1)
    if(len(split_filename) > 1):  # 包含一层文件夹
        if(not os.path.exists(split_filename[0])):
            os.mkdir(split_filename[0])


def get_json_data(filename, template_json_str):
    check_directory(filename)
    if(os.path.exists(filename) and os.path.getsize(filename) != 0):
        with open(filename, 'r', encoding='utf-8') as j:
            try:
                json_data = json.load(j)
            except Exception as e:
                print(filename, "解析错误：", str(e))
                print("请检查", filename, "信息")

                # # 打开非 user status 文件可能造成问题。
                # # ✨ U****** 不让改 5555~~~
                # if 'user_status.json' in filename:
                #     print("正在尝试修复", filename)
                #     new = []
                #     error_line_index = 8
                #     with open(filename, 'r', encoding='utf-8') as conf:
                #         for line in conf:
                #             new.append(line)
                #         print(new[error_line_index+1])
                #         if '},' in new[error_line_index+1] and '"0":"default"' in new[error_line_index-1]:
                #             print(new[error_line_index-1])
                #             # 一般错误为'        "0":"default"\n' 
                #             new[error_line_index-1] = new[error_line_index-1][:-1]+',\n'
                #             new[error_line_index] = ''
                #             new[error_line_index+1] = ''
                #     with open(filename, 'w', encoding='utf-8') as conf:
                #         for line in new:
                #             conf.write(line)

                exit(-1)
    else:
        json_data = json.loads(template_json_str)
    return json_data


def save_json_data(filename, object_to_save, sort_keys=True):
    check_directory(filename)
    with open(filename, 'w', encoding='utf-8') as o:
        json.dump(object_to_save, o, sort_keys=True, indent=4,
                  separators=(',', ':'), ensure_ascii=False)


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
    with open(filename, 'w', encoding='utf-8') as o:
        o.write(text)
