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
data_path = '/Users/ekaterinakozakova/Desktop/dev/mysite/data/data.txt'
res_path = '/Users/ekaterinakozakova/Desktop/dev/mysite/data/results.txt'
users_path = '/Users/ekaterinakozakova/Desktop/dev/mysite/data/users.txt'


def get_cards(lesson_id: int) -> list[Card]:
    f = open(data_path, 'r')
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


def cards_to_tuple_with_pics(cards: list[Card]):
    res = []
    for card in cards:
        pic = "Null.png"  # TODO: picture with 'no data'
        if card.pic_name != "NONE":
            pic = card.pic_name
        res.append([card.lesson_id, card.lesson, card.word, card.translation, pic])
    return res


def add_cards(cards: list[Card]) -> None:
    f = open(data_path, 'a')
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


def get_users() -> {str: str}:
    f = open(users_path, 'r')
    res = {}
    for line in f:
        line_data = line.split(sep)
        if len(line_data) != 2:
            continue
        res[line_data[0]] = line_data[1]
    return res


def get_password(user: str) -> str | None:
    user_passes = get_users()
    if user not in user_passes:
        return None
    return user_passes[user]


# def add_result():
#     f = open(res_path, 'r')
#     result = []
#     for line in f:
#         line_result = line.split(sep)
#         if len(line_result) < 5:
#             continue
#         i = int(line_result[0])
#         if i != lesson_id:
#             continue
#         result.append(email, Card(i+1, line_result[1], line_result[2], line_result[3], line_result[4]))
#     return result
