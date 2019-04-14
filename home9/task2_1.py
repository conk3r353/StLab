from PIL import Image, ImageOps
import datetime
import os
from multiprocessing import Process, Manager


class MyProcess(Process):
    def __init__(self, obj_list, flag_list):
        super().__init__()
        self.obj_list = obj_list
        self.flag_list = flag_list

    def run(self):
        for obj in self.obj_list:
            self.flag_list.append(modify_pic(obj))


def main_process():
    flag_list = Manager().list()
    flags = []

    for flag in os.listdir('flags'):
        flags.append(flag)

    processes = [MyProcess(flags[:62], flag_list),
                 MyProcess(flags[62:124], flag_list),
                 MyProcess(flags[124:186], flag_list),
                 MyProcess(flags[186:], flag_list)]

    start = datetime.datetime.now()

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print(f'C процессами: {datetime.datetime.now() - start}')

    print(flag_list)


def modify_pic(name):
    img = Image.open(f'flags/{name}')
    border_img = ImageOps.expand(img, border=1, fill='black')
    border_img.save(f'flags_plus/{name}')
    img_size = os.stat(f'flags/{name}').st_size
    border_img_size = os.stat(f'flags_plus/{name}').st_size
    return name.split('.')[0], img_size, border_img_size


if __name__ == '__main__':
    main_process()
