#!/bin/bash

update() {
    echo "下载更新"
    git -C /xuexi/code/TechXueXi pull $Sourcepath $pullbranche
    echo "下载完毕"
    cp -r /xuexi/code/TechXueXi/SourcePackages/* /xuexi
    echo "更新完成"
}

if [[ ${pullbranche} == "developing" ]]; then
    echo "当前处于开发模式，自动更新"
    update
fi
#echo "检查更新"
#git -C /xuexi/code/TechXueXi pull $Sourcepath $pullbranche
#echo "检查更新完毕"
#cp -r /xuexi/code/TechXueXi/SourcePackages/* /xuexi
echo "开始运行"
/usr/local/bin/python /xuexi/pandalearning.py
