#!/bin/sh
cd /xuexi/code/TechXueXi
echo "检查更新"
git pull $Sourcepath $pullbranche
echo "检查更新完毕"
cp -r /xuexi/code/TechXueXi/SourcePackages/* /xuexi
echo "开始运行"
cd /xuexi
python ./pandalearning.py