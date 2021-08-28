#!/bin/sh
cd /xuexi/code/TechXueXi
echo "检查更新"
git pull
echo "检查更新完毕"
cp -r /xuexi/code/TechXueXi/SourcePackages/* /xuexi
cd /xuexi/code
echo "开始运行"
python pandalearning.py > /proc/1/fd/1