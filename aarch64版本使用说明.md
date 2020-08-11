在aarch64设备上将v2.5版本的源码打包成了可执行文件：pandalearning-aarch64

在斐讯N1@Ubuntu18.04上测试可以正常运行

理论上运行linux的aarch64的设备，在安装了chromiumdriver和chromium-browser后，可以正常执行

ubuntu运行示例：
安装chromium-chromedriver和chromium-browser
```
apt-get update
apt-get install chromium-chromedriver
```
执行aarch64的可执行文件：
```
./pandalearning-aarch64
```