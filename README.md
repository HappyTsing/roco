# roco

虽然洛克王国的任务可以使用悟空辅助解决，但仍旧需要等待任务完成才能进行下一个任务，令人苦恼！


本脚本正是为了解决该问题而存在，通过图像识别自动等待任务结束，一键完成诸多功能，例如魔法先锋队的一阶形态、暗黑城日常等，通过简单配置 `config.yaml` 文件，可以自定义更多功能。


支持的任务：

1. 【日常】 洛克寻宝 - 乐园探险 - 暗黑城日常
2. 【常驻】 魔法先锋队一阶任务
3. 【其他】 好友庄园助手 - 星辰塔扫荡

支持的屏幕分辨率：

- `1920*1080`
- `1360*768`，

其余分辨率需要自行截图，并替代 `\img` 中对应的图片。

# quick start

```sh
# python 3.8.10

# pytorch https://pytorch.org/get-started/locally/

pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

python3 main.py
```


# pck

自行打包

```sh
pyinstaller -F main.py
```

上述方式打包后运行较慢，采用 `-D` 打包多文件，再使用 [Enigma Virtual Box](https://enigmaprotector.com/en/downloads.html) 将其压缩为可执行文件。

```sh
pyinstaller -D main.py
# Enigma Virtual Box  再次压缩
```
