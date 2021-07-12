# Fedora/openSUSE快速使用Panda-Learning方法
## Fedora/openSUSE快速安装Chrome和ChromeDriver
### 1.配置Google Chrome源
`cp google-chrome.repo /etc/yum.repos.d/`
### 2.安装Chrome和ChromeDriver
`dnf install google-chrome-stable`

`dnf install chromedriver`

此方法既快速又可避免缺少依赖造成的安装失败

Fedora默认将chrome安装在/opt/google/chrome/

默认将chromedriver安装在/usr/lib64/chromium-browser/

### 注意：chromium ≠ chrome 试图安装使用chromium替代chrome的同学，可能会无法学 xi ！
## 安装Python的WebDriver组件
`pip3 install selenium`

`pip3 install requests`

## 运行Panda-Learning源码
`python3 pandalearning.py`
