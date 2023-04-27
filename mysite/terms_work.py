from . import core


def write_word_with_translation(lesson_id, lesson, word, translation):
    new_card = core.Card(lesson_id, lesson, word, translation, 'NONE')
    core.add_cards([new_card])
