from . import core


def get_terms_for_table():
    terms = []
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        cnt = 1
        for line in f.readlines()[1:]:
            term, definition, source = line.split(";")
            terms.append([cnt, term, definition])
            cnt += 1
    return terms


def write_word_with_translation(lesson_id, lesson, word, translation):
    new_card = core.Card(lesson_id, lesson, word, translation, 'NONE')
    core.add_cards([new_card])
    # new_term_line = f"{new_term};{new_definition};user"
    # with open("./data/terms.csv", "r", encoding="utf-8") as f:
    #     existing_terms = [l.strip("\n") for l in f.readlines()]
    #     title = existing_terms[0]
    #     old_terms = existing_terms[1:]
    # terms_sorted = old_terms + [new_term_line]
    # terms_sorted.sort()
    # new_terms = [title] + terms_sorted
    # with open("./data/terms.csv", "w", encoding="utf-8") as f:
    #     f.write("\n".join(new_terms))


def get_terms_stats():
    db_terms = 0
    user_terms = 0
    defin_len = []
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            term, defin, added_by = line.split(";")
            words = defin.split()
            defin_len.append(len(words))
            if "user" in added_by:
                user_terms += 1
            elif "db" in added_by:
                db_terms += 1
    stats = {
        "terms_all": db_terms + user_terms,
        "terms_own": db_terms,
        "terms_added": user_terms,
        "words_avg": sum(defin_len)/len(defin_len),
        "words_max": max(defin_len),
        "words_min": min(defin_len)
    }
    return stats
