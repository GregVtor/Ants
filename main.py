import json
import os
from PIL import Image
from time import time


if not os.path.exists('config.json'):
    print('Нет файла конфигурации, запустите Configurate.py')
    exit()

with open('config.json', 'r') as fp:
    config = json.load(fp)

if not os.path.exists(config['files_patch']):
    os.mkdir(config['files_patch'])

from Classes import Board

b = Board(config['board_size'], config['ant_count'], config)

for i in range(config['frames_count']):
    s = time()
    b.update()
    img = Image.new('RGB', config['board_size'], 'black')
    img_l = img.load()
    for w in range(b.size[0]):
        for h in range(b.size[1]):
            if b.pher_cart[w][h] <= 255:
                img_l[w, h] = 0, b.pher_cart[w][h], 0
            elif b.pher_cart[w][h] <= 510:
                img_l[w, h] = 0, 255, b.pher_cart[w][h] - 255
            elif b.pher_cart[w][h] <= 765:
                img_l[w, h] = b.pher_cart[w][h] - 510, 255, 255
            else:
                img_l[w, h] = 255, 255, 255
    img.save(os.path.join(config["files_patch"], f'{i}.png'))
    print(time() - s, i)
