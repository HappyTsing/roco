# roco (不再维护)

虽然洛克王国的任务可以使用悟空辅助解决，但仍旧需要等待任务完成才能进行下一个任务，令人苦恼！


本脚本正是为了解决该问题而存在，通过图像识别自动等待任务结束，一键完成诸多功能，通过简单配置 `config.yaml` 文件和相对应的 `\img`，还可以自定义更多功能。


## Prepare

首先在本地精灵仓库配置好名为 **fz** 的队伍，首发精灵必须为 **魔神武王**，其余五个请选择双攻尽可能高的宠物。


## Usage


解压缩 release 的文件夹，打开 `悟空神辅`，双击 `main_boxed.exe`，脚本将自动依次执行：

1.  【双攻大队-魔神武王】 自动切换队伍
2.  【日常任务】 
3.  【常驻任务】 
4.  【取物助手】
5.  【星辰之塔】
6.  【黄道十二宫 一阶】
7.  【七曜圣地】
8.  【失落之塔】
9.  【钻石任务】
10. 【好友庄园助手】

若不想执行某条任务，编辑 `config.yaml -> tasks`，将对应的任务设置为 `enable: off` 即可。

支持的屏幕分辨率：

- `1920*1080`
- `1360*768`，

其余分辨率需要自行截图，并替代 `\img` 中对应的图片。

## Quick start

若想运行源代码版本，可进行如下操作：

```sh
# python 3.8.10

# pytorch https://pytorch.org/get-started/locally/

pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

python3 main.py
```

> 建议直接使用打包好的 release 版本，双击 `exe` 文件即可运行。

## Package

若想自行打包，可进行如下操作：

```sh
# 打包单个 exe 文件
pyinstaller -F main.py
```

上述方式打包后运行较慢，建议采用 `-D` 打包多文件，再使用 [Enigma Virtual Box](https://enigmaprotector.com/en/downloads.html) 将其压缩为可执行文件。

```sh
pyinstaller -D main.py
# Enigma Virtual Box  再次压缩
```
