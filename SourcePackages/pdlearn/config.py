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


def get_env_or_cfg(key, env_key=None, def_value=None):
    """
    获取环境变量，或者配置信息。优先获取环境变量

    @param key: 配置信息的key，例：display.banner、addition.TG_SendQRImage、addition.Tg.sendMsg
    @param env_key: 环境变量key，如果不填则使用key的最后一节，如。key=addition.TG_SendQRImage，则env_key=TG_SendQRImage，则env_key
    @param def_value: 如果配置获取失败，返回默认值
    """
    if not env_key:
        env_key = key.split(".")[-1]
    if os.getenv(env_key):
        return os.getenv(env_key)
    else:
        return cfg_get(key, def_value)
