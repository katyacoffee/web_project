from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse
from . import terms_work, core
import json


unknown_guest = "unknown guest"


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
    words = core.cards_to_tuple_with_pics(core.get_all_cards())
    return render(request, "cards.html", context={"words": words})


def test(request):
    words = core.cards_to_tuple(core.get_all_cards())
    return render(request, "test.html", context={"words": words})


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


def send_answers(request):
    if request.method == "POST":
        cache.clear()
        lesson_id = request.POST.get("lesson_id")
        user_name = request.POST.get("user_login")
        if user_name == "":
            user_name = unknown_guest
        context = {"user": user_name, "lesson_id": lesson_id}
        cards_for_lesson = core.get_cards(int(lesson_id))
        context["success"] = True
        points = 0
        for card in cards_for_lesson:
            answer = request.POST.get("answer_" + card.word)
            # if len(answer) == 0:
            #     context["success"] = False
            #     context["comment"] = "Слово должно быть не пустым. Вы забыли перевод '" +\
            #                          card.translation + "'."
            #     break
            if answer.lower() == card.word.lower():
                points += 1
        if context["success"]:
            context["success-title"] = "Тест успешно заполнен"
            context["comment"] = "Тест пройден с результатом " +\
                                 f'{points}/{len(cards_for_lesson)}'
            if user_name is not unknown_guest:
                core.add_result(user_name, int(lesson_id), points/len(cards_for_lesson))
        return render(request, "test_request.html", context)
    else:
        add_term(request)


def submit_login(request):
    data = json.loads(request.body)
    user = data['title']
    pwd = data['body']
    if user == "":
        return HttpResponse("Имя пользователя не заполнено.")
    print(user, pwd)
    correct_pwd = core.get_password(user)
    if correct_pwd is None:
        return HttpResponse("Пользователь '" + user +
                            "' не найден. Пожалуйста, зарегистрируйтесь.")
    elif correct_pwd != pwd:
        return HttpResponse("Неверный пароль для пользователя '" + user + "'!")
    return HttpResponse("TRUE")


def show_stats(request):
    stats = terms_work.get_terms_stats()
    return render(request, "stats.html", stats)
