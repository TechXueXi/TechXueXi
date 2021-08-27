#!/bin/sh
cd code
cd TechXueXi
echo "检查更新"
git pull
echo "检查更新完毕"
cd ..
cp -r TechXueXi/SourcePackages/* ..
cd ..
python pandalearning.py > /proc/1/fd/1