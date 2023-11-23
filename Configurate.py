import json
import os


DEFOLT = {
        'pher_volatilization': 10,
        'pher_trace': 50,
        'ant_crazy_limit': 255,
        'ant_crazy_time': 10,
        'ant_speed_range': (-1, 1),
        'board_size': (500, 500),
        'ant_count': 6000,
        'ant_turn_angle_range': (0, 90),
        'sensors_angle_range': (0, 120),
        'ant_sensor_len_range_relative_to_speed': (1, 25),
        'file_name_ant_spawn_pattern': None,
        'file_name_pher_pattern': None,
        'frames_count': 2000,
        'files_patch': os.path.join('data'),
    }


def crate_conf(data):
    if isinstance(data, str):
        return json.dump(DEFOLT, open('config.json', 'w'), ensure_ascii=False)
    return json.dump(data, open('config.json', 'w'), ensure_ascii=False)


if __name__ == '__main__':
    print('''                          ▄▄               
          ██                  ██   ██          
         ▄██▄                      ██          
        ▄█▀██▄   ▀████████▄ ▀███ ██████ ▄██▀███
       ▄█  ▀██     ██    ██   ██   ██   ██   ▀▀
       ████████    ██    ██   ██   ██   ▀█████▄
      █▀      ██   ██    ██   ██   ██   █▄   ██
    ▄███▄   ▄████▄████  ████▄████▄ ▀██████████▀
    beta pre 1                                           
    ''')

    print('Привет, это конфигуратор, здесь вы можете настроить своё поле и муравьёв.\n')
    print('Приступим\n')
    if input('Желаешь загрузить дефолтные настройки[Y/N]?: ').lower() == 'y':
        crate_conf('')
        exit()
    data = DEFOLT.copy()
    for key in data.keys():
        a = input(f'Введите {key}, либо оставте стандартный. Пример: {DEFOLT[key]}: ')
        if isinstance(data[key], int):
            data[key] = int(a)
        elif isinstance(data[key], tuple):
            data[key] = [int(i) for i in a[1:-1].replace(',', '').split()]
        elif a.lower() == 'none':
            data[key] = None
        else:
            data[key] = a
    crate_conf(data)
