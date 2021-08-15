import os
import sys

def try_import_all_module():
    import requests
    import lxml
    import colorama
    import bs4
    import selenium
    import pyhocon
    pass

def check_environment():
    """
    注：此函数仅能在 pandalearning.py 开头处调用，进行初始化操作
    """
    # ====================切换pwd到python文件路径====================
    # 切换pwd到python文件路径，避免找不到相对路径下的ini和相关文件
    # 注：不要再pandalearning.py之外使用os.chdir(sys.path[0])，否则可能造成打包程序不能运行
    base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    os.chdir(base_path)
    # ===============requirements.txt模块自检====================
    try:
        try_import_all_module()
    except ImportError as e:
        print(str(e))
        print("检测到你有python模块找不到，你可在搜索引擎搜索安装相关模块。")
        print("或转到上一级目录，运行：pip3 install -r requiremes.txt 或 pip install -r requirements.txt")
        print("下面为你尝试自动安装requirement.txt")
        input("如需自动安装按回车键继续...（如不需要自动尝试安装可现在关闭程序）")
        try:
            from pip._internal import main as pip_main
            pip_main(['install', '-r', '../requirements.txt'])
        except Exception as e:
            print(str(e))
            print("尝试自动安装requirement.txt失败，请手动安装并反馈此报错信息")
            input("按回车键退出程序......")
            exit(333)