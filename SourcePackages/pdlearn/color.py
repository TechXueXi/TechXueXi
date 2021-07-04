import colorama
from colorama import Fore, Back, Style # 命令行颜色字体库
colorama.init(autoreset=True) # 使旧版cmd中命令行颜色字体生效, 并在print换行处自动还原默认颜色

def red(some_str):
    return Fore.LIGHTRED_EX + some_str + Fore.RESET

def yellow(some_str):
    return Fore.YELLOW + some_str + Fore.RESET

def blue(some_str):
    return Fore.LIGHTBLUE_EX + some_str + Fore.RESET

def green(some_str):
    return Fore.GREEN + some_str + Fore.RESET