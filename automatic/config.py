# -*-coding:UTF-8 -*-
from yaml import safe_load
from os import path
from loguru import logger
import tkinter
import sys

if getattr(sys,'frozen',False):
    # pyinstaller
    CUR_PATH = path.dirname(path.realpath(sys.argv[0]))
else:
    CUR_PATH = path.dirname(path.abspath(__file__))
    
CONFIG_PATH = path.join(CUR_PATH,"config.yaml")
IMAGE_PATH = path.join(CUR_PATH,"img")

# 获取屏幕分辨率
screen = tkinter.Tk()
x = screen.winfo_screenwidth()
y = screen.winfo_screenheight()
screen.destroy()
logger.info('屏幕分辨率: ({},{})'.format(x, y))
IMG_PATH = path.join(CUR_PATH, "img", "{}_{}".format(x,y))
if not path.exists(IMG_PATH):
    logger.error("未适配当前分辨率，请自行添加模板图片!")
else:
    logger.success("当前屏幕分辨率已适配!")
    
"""
解析配置文件，返回任务列表
"""


def config_parser(config):
    parent_phases = config["parent_phases"]
    tasks = config["tasks"]
    new_tasks = {}
    task_name_list = []
    for task in tasks:
        parent_phases_name = task.get("parent_phase")
        phases = task.get("phases")
        task_name = task.get("name_en")
        task_name_list.append(task_name)
        is_parent = False
        new_phases = []
        while True:
            # 反转列表
            temp = phases[::-1]
            phases = temp
            if is_parent:
                dir_name = "parent_phases"
            else:
                dir_name = "tasks"
                is_parent = True

            for phase in phases:
                template = path.join(
                    IMG_PATH, dir_name, task_name, str(phase['id'])+".png")
                new_phase = {}
                new_phase.update(phase)
                new_phase.pop("id")
                if phase['action'] != "press":
                    new_phase["template"] = template
                # new_phase = {
                #     "name": phase['name'],
                #     "action": phase['action'],
                #     "template": template
                # }
                # 插到列表最前面
                new_phases.insert(0, new_phase)
            # 循环退出条件
            if parent_phases_name == None:
                break
            p_task = parent_phases[parent_phases_name]
            task_name = parent_phases_name
            parent_phases_name = p_task.get("parent_phase")
            phases = p_task.get("phases")
        new_task = {
            "name": task.get("name"),
            "name_en": task.get("name_en"),
            "phases": new_phases
        }
        new_tasks[task.get("name_en")] = new_task
    return new_tasks,task_name_list


with open(CONFIG_PATH, 'r', encoding='utf-8') as _fp:
    config = safe_load(_fp)
    tasks,task_name_list = config_parser(config)
    # logger.info(tasks)

if __name__ == '__main__':
    pass
