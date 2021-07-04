import os
import sys
from pdlearn.initial import *
from configparser import ConfigParser

cfg = ConfigParser()

#os.chdir(sys.path[0]) # 切换pwd到python文件路径，避免找不到相对路径下的ini
base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(base_path)
if(not os.path.exists("config")):
    os.mkdir("config")
if(not os.path.exists("./config/main.ini")):
    init_main_ini()
    # input("缺少配置文件 config/main.ini，请检查. 按回车键退出程序. ")
    # exit()
cfg.read('./config/main.ini', encoding='utf-8')


# def write_default_ini():
#     ini_str = '''（从main.ini复制过来，如无main.ini则写入。但如果有main.ini而新版又更新了ini项目，合并就比较困难）'''
