import math
import random
import os

from PIL import Image
from nonebot import logger
from pathlib import Path

SEP = os.sep
RES_PATH = str(Path(__file__).parent) + SEP + "res"


def generate_avatar():
    correct_id = random.randint(1001, 1100)
    var_offset = random.randint(1, 4)
    file_path = "file:///" + RES_PATH + SEP + "f_" + "{:04d}".format(correct_id) + "_" + str(
        var_offset) + ".png"
    return correct_id, file_path


def crop_img(file_path, group_id):
    img = Image.open(file_path.split("///")[1])

    logger.debug(img.size)
    (width, height) = img.size
    left = math.floor(random.random() * (width - 0.28 * width))
    bottom = math.floor(random.random() * (height - 0.28 * height))

    cropped = img.crop((left, bottom, left + 0.28 * width, bottom + 0.28 * height))
    save_path = RES_PATH + SEP + "tmp" + SEP + "crop_" + str(group_id) + ".png"
    cropped.save(save_path)

    return "file:///" + save_path


class Game_monitor:
    def __init__(self):
        self.game_tokens = {}
        self.game_answers = {}
        self.game_ans_path = {}

    def game_start(self, group_id):
        self.game_tokens[group_id] = True
        (correct_id, file_path) = generate_avatar()
        self.game_answers[group_id] = correct_id
        self.game_ans_path[group_id] = file_path
        return file_path

    def game_set(self, group_id):
        self.game_tokens[group_id] = False

    def game_status(self, group_id):
        return self.game_tokens[group_id] if self.game_tokens.get(group_id) is not None else False

    def get_correct_answer(self, group_id):
        return self.game_answers[group_id] if self.game_answers.get(group_id) is not None else -1

    def get_correct_img(self, group_id):
        return self.game_ans_path[group_id] if self.game_ans_path.get(group_id) is not None else "Img not found ERROR"
