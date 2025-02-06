# File2Vid
This software is not available in languages other than Chinese and English.

使用nuitka编译了，解压运行main.exe即可

https://www.123865.com/s/CndUjv-mVGVh?
提取码:f2vd

## 程序简介
 这是一个基于 Python 的脚本，用于将任何文件转换为视频和音频，并将它们合并为一个完整的视频文件。它利用了 `ffmpeg-python` 等工具实现文件的转换和处理。

## 功能特点
- 将任何文件转换为有声音的视频。
- 会对视频放大处理。
- 提供图形化界面提示和交互。
- <font size="1">挺精简的？</font>

### 下载
`git clone https://github.com/nbk888/File2Vid.git`


### 运行步骤
- 建议使用anaconda等虚拟环境
`conda create -n file2vid python=3.10`
`activate file2vid`

`cd File2Vid`

1. 安装ffmpeg:（如果已安装可以跳过）
https://www.gyan.dev/ffmpeg/builds/ 下载ffmpeg-git-essentials.7z
将其解压到某个目录
打开 编辑系统环境变量 系统变量 => 双击Path => 新建 => (解压的ffmpeg路径)\bin\
打开cmd测试 ffmpeg -version 如果有版本号则安装成功
如果没有版本号 请按照这篇文章再详细安装 https://blog.csdn.net/Natsuago/article/details/143231558


1. 安装依赖库：`pip install -r requirements.txt` 
2. 运行脚本：``python main.py``
3. 按照图形界面提示选择文件并输入相关信息。
4. 等待程序运行完成，生成的视频文件将保存在脚本所在目录。

## 注意事项
- 不要在程序运行时删除临时文件，否则可能导致程序出错。
- 生成的视频和音频质量可能因输入文件内容而异。

实例：【DISKGENIUS】https://www.bilibili.com/video/BV1gcfUYCEZH?vd_source=cd6fa57d3811995477c415f2a801e8bd

如果有bug欢迎发布issue讨论！    
