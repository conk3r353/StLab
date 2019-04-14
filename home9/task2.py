from PIL import Image, ImageOps
import datetime
import os
from multiprocessing import Process, Manager


class MyProcess(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        modify_pic(self.name)


def main_process():
    start = datetime.datetime.now()
    objects = Manager().Queue()
    processes = list()
    # length = len(os.listdir('flags'))

    for flag in os.listdir('flags'):
        objects.put(MyProcess(flag))

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print(f'C процессами: {datetime.datetime.now() - start}')

    # return result


# def modify_pic(name):
    # img = Image.open(f'flags/{name}')
    # border_img = ImageOps.expand(img, border=1, fill='black')
    # border_img.save(f'flags_plus/{name}')
    # img_size = os.stat(f'flags/{name}').st_size
    # border_img_size = os.stat(f'flags_plus/{name}').st_size
    # # return_list.append((name.split('.')[0], img_size, border_img_size))
    # queue.put((name.split('.')[0], img_size, border_img_size))


def modify_pic_linear(name):
    img = Image.open(f'flags/{name}')
    border_img = ImageOps.expand(img, border=1, fill='black')
    border_img.save(f'flags_extra/{name}')
    img_size = os.stat(f'flags/{name}').st_size
    border_img_size = os.stat(f'flags_extra/{name}').st_size
    return name.split('.')[0], img_size, border_img_size


def linear_modification():
    start = datetime.datetime.now()
    result = list()
    for flag in os.listdir('flags'):
        result.append(modify_pic_linear(flag))
    print(f'Без процессоров: {datetime.datetime.now() - start}')
    return result


if __name__ == '__main__':
    print(linear_modification())
    # print(main_process())
