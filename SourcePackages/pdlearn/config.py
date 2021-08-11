import os
import sys
from pdlearn import file

conf_template_text = '''include required(file("../config/default_template.conf"))\n\n\n\n'''

cfg = file.get_conf_file("user/settings.conf", conf_template_text)


