from django.shortcuts import render
from django.core.cache import cache
from . import terms_work, core


def index(request):
    return render(request, "index.html")


def terms_list(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def lessons_list(request):
    words = core.cards_to_tuple(core.get_all_cards())
    return render(request, "lessons_list.html", context={"words": words})


def lessons(request):
    lessons = core.get_lessons()
    return render(request, "lessons.html", context={"lessons": lessons})


def cards(request):
    cards = core.get_cards()
    return render(request, "cards.html")
# TODO доделать!!!


def test(request):
    test = core.cards_to_tuple(core.get_all_cards())
    return render(request, "test.html")
# TODO доделать!!!


def add_term(request):
    return render(request, "term_add.html")


def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        lesson_id = request.POST.get("lesson_id", "")
        lesson = request.POST.get("lesson", "")
        word = request.POST.get("new_term", "")
        translation = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(translation) == 0:
            context["success"] = False
            context["comment"] = "Перевод должен быть не пустым"
        elif len(word) == 0:
            context["success"] = False
            context["comment"] = "Слово должно быть не пустым"
        elif len(lesson_id) == 0 or not lesson_id.isnumeric() or int(lesson_id) <= 0:
            context["success"] = False
            context["comment"] = "Номер урока должен быть целым положительным числом"
        elif len(lesson) == 0:
            context["success"] = False
            context["comment"] = "Тема урока должна быть не пустой"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_work.write_word_with_translation(lesson_id, lesson, word, translation)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term(request)


def show_stats(request):
    stats = terms_work.get_terms_stats()
    return render(request, "stats.html", stats)
