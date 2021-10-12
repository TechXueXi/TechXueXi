import os
import sys
from pdlearn import file

conf_template_text = '''include required(file("../config/default_template.conf"))\n\n\n\n'''

# from pdlearn.config import cfg 是只读变量
cfg = file.get_conf_file("user/settings.conf", conf_template_text)


def cfg_get(key, def_value=None):
    """
    获取基础配置

    @param key: 配置信息的key，例：display.banner、addition.TG_SendQRImage、addition.Tg.sendMsg
    @param def_value: 如果配置获取失败，返回默认值
    """
    try:
        return cfg.get(key)
    except:
        return def_value
