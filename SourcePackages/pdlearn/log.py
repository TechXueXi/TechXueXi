import datetime

def log_timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def log_daily(text):
    text = text+"\n"
    with open("user/daily.log", "a", encoding = 'utf-8') as f:
        f.write(text)

