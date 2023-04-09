from dataclasses import dataclass
import os


@dataclass
class Card:
    lesson_id: int
    lesson: str
    word: str
    translation: str
    pic_name: str


no_pic = 'NONE'
sep = '|'
# TODO: fix to relpath
file_path = '/Users/ekaterinakozakova/Desktop/dev/mysite/data/data.txt'


def get_cards(lesson_id: int) -> list[Card]:
    f = open(file_path, 'r')
    res = []
    for line in f:
        line_data = line.split(sep)
        if len(line_data) < 5:
            continue
        i = int(line_data[0])
        if i != lesson_id:
            continue
        res.append(Card(i, line_data[1], line_data[2], line_data[3], line_data[4]))
    return res


def get_all_cards() -> list[Card]:
    i = 1
    res = []
    while i < 100:
        data = get_cards(i)
        if len(data) == 0:
            break
        res.extend(data)
        i += 1
    return res


def cards_to_tuple(cards: list[Card]):
    res = []
    for card in cards:
        res.append([card.lesson_id, card.lesson, card.word, card.translation])
    return res


def add_cards(cards: list[Card]) -> None:
    f = open(file_path, 'a')
    if len(cards) > 0:
        f.write('\n')
    for card in cards:
        line = f'{card.lesson_id}' + sep + \
               card.lesson + sep + \
               card.word + sep + \
               card.translation + sep + \
               card.pic_name + sep
        f.write(line)


def get_lessons():
    i = 1
    res = []
    while i < 100:
        data = get_cards(i)
        if len(data) == 0:
            break
        res.append([data[0].lesson_id, data[0].lesson])
        i += 1
    return res
