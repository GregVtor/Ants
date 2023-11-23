import numpy as np
from PIL import Image
from math import sin, cos
from random import randint, random


def create_turn_matrix(angle):
    return np.array([[cos(angle), -sin(angle)], [sin(angle), cos(angle)]])


class Board:
    def __init__(self, size, ant_count, config):
        self.pher_cart = np.zeros(size, dtype=int)
        self.ants = []
        self.size = size
        self.config = config

        if not config['file_name_ant_spawn_pattern']:
            for _ in range(ant_count):
                self.ants.append(Ant([randint(0, size[0] - 1), randint(0, size[1] - 1)], self))
        else:
            a_p = Image.open(config['file_name_ant_spawn_pattern'])
            a_p_l = a_p.load()
            for i in range(a_p.width):
                for j in range(a_p.height):
                    if sum(a_p_l[i, j]) != 0:
                        self.ants.append(Ant([i, j], self))

        if config['file_name_pher_pattern']:
            f_p = Image.open(config['file_name_pher_pattern'])
            f_p_l = f_p.load()
            for i in range(f_p.width):
                for j in range(f_p.height):
                    if sum(f_p_l[i, j]) != 0:
                        self.pher_cart[i][j] = 255

    def update(self):
        self.pher_cart = self.pher_cart - self.config['pher_volatilization']
        self.pher_cart = np.clip(self.pher_cart, 0, 10000)

        for ant in self.ants:
            ant.update()


class Ant:
    def __init__(self, coords: list[int, int], board):
        self.board = board

        self.vector = np.array(
            [randint(*self.board.config['ant_speed_range']), randint(*self.board.config['ant_speed_range'])])  # Pheromone motion
        self.turn_angle = randint(*self.board.config['ant_turn_angle_range'])  # Angle of rotation of the
        self.turn_dict = {'1': -self.turn_angle, '2': 0, '3': self.turn_angle}
        self.sensor2_vector = self.vector * random() * randint(*self.board.config['ant_sensor_len_range_relative_to_speed'])
        self.sensor_angle = randint(*self.board.config['sensors_angle_range'])  # The angle between the three ant sensors

        self.coords = coords

        self.sensor1_vector = np.dot(create_turn_matrix(-self.sensor_angle),
                                     self.sensor2_vector)
        self.sensor3_vector = np.dot(create_turn_matrix(self.sensor_angle),
                                     self.sensor2_vector)
        self.crazy = 0

    def update(self):
        turn_angle = self.sensor_work()
        new_coords = self.move(turn_angle)
        normalize = self.vector / self.board.config['ant_speed_range'][1]
        painted = []
        if normalize[0] + normalize[1] == 0:
            quantly = 0
        elif normalize[0] == 0:
            quantly = int(self.vector[1] / normalize[1])
        elif normalize[1] == 0:
            quantly = int(self.vector[0] / normalize[0])
        else:
            quantly = int(self.vector[1] / normalize[1])
        for inter in range(quantly):
            width, height = np.array(self.coords + (normalize * inter),
                                     dtype=int)
            width = self.tp_cord(width, True)
            height = self.tp_cord(height, False)
            if [width, height] not in painted:
                self.board.pher_cart[width][height] += self.board.config['pher_trace']
                painted.append([width, height])
        self.coords = [self.tp_cord(new_coords[0], True), self.tp_cord(new_coords[1], False)]

    def move(self, turn_angle: int) -> list[int, int]:
        turn_matrix = create_turn_matrix(turn_angle + random() * 10)
        self.vector = np.dot(turn_matrix, self.vector)
        return np.array(self.coords) + self.vector

    def tp_cord(self, cord: int, w_or_h: bool) -> int:
        maxim = self.board.size[0] if w_or_h else self.board.size[1]
        if cord < 0:
            return maxim + cord
        elif cord > maxim:
            return cord - maxim
        elif cord == maxim:
            return 0
        else:
            return cord

    def sensor_work(self) -> int:
        sensor1_cords = np.array(self.coords + self.sensor1_vector, dtype=int)
        sensor1_data = self.board.pher_cart[self.tp_cord(sensor1_cords[0], True)][self.tp_cord(sensor1_cords[1], False)]

        sensor2_cords = np.array(self.coords + self.sensor2_vector, dtype=int)
        sensor2_data = self.board.pher_cart[self.tp_cord(sensor2_cords[0], True)][self.tp_cord(sensor2_cords[1], False)]
        if sensor2_data > self.board.config['ant_crazy_limit']:
            self.crazy = self.board.config['ant_crazy_time']

        sensor3_cords = np.array(self.coords + self.sensor3_vector, dtype=int)
        sensor3_data = self.board.pher_cart[self.tp_cord(sensor3_cords[0], True)][self.tp_cord(sensor3_cords[1], False)]

        if self.crazy:
            direction = sorted(
                [["1", sensor1_data], ["2", sensor2_data],
                 ["3", sensor3_data]],
                key=lambda x: -x[1])[0][0]
            self.crazy -= 1
        else:
            direction = sorted(
                [["1", sensor1_data], ["2", sensor2_data],
                 ["3", sensor3_data]])[0][0]
        return self.turn_dict[direction]
