#!/bin/sh
echo "检查更新"
git -C /xuexi/code/TechXueXi pull $Sourcepath $pullbranche
echo "检查更新完毕"
cp -r /xuexi/code/TechXueXi/SourcePackages/* /xuexi
echo "开始运行"
nohup python3 /xuexi/pandalearning.py >> script_log.log 2>&1& exit 0