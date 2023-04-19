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
    lines = f.read().splitlines()
    for line in lines:
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


def get_all_results() -> {str: list[float]}:
    f = open(res_path, 'r')
    res = {}
    lines = f.read().splitlines()
    for line in lines:
        line_data = line.split(sep)
        if len(line_data) < 2:
            continue
        results = []
        for i, r in enumerate(line_data):
            if i == 0:
                continue
            try:
                r = float(r)
            except ValueError:
                r = 0.0
            results.append(r)
        res[line_data[0]] = results
    return res


def add_result(user: str, lesson_id: int, points: float):
    all_results = get_all_results()
    if user not in all_results.keys():
        user_results = []
        for _ in [1, lesson_id]:
            user_results.append(0.0)
        user_results.append(points)
        all_results[user] = user_results
    else:
        user_results = all_results[user]
        user_results[lesson_id-1] = points
        all_results[user] = user_results

    f = open(res_path, 'w')
    for u in all_results.keys():
        f.write(make_str_of_results(u, all_results[u]))
    f.close()


def make_str_of_results(user: str, results: list[float]) -> str:
    res = user
    for r in results:
        res += f'|{r}'
    res += '\n'
    return res

