# -*- coding: utf-8 -*-
from math import sqrt
import matplotlib.pyplot as plt
import isbnlib
from nose.plugins.skip import SkipTest
from nose.tools import nottest


def getBooksNumber():
    i = 0
    for l in open('./data/BX-CSV-Dump/BX-Books.csv'):
        i = i + 1

    print(i)

# Загрузка данных (пример для movielen)


def load_data(path='./data/BX-CSV-Dump/BX-Book-Ratings.csv'):
    # загружаем предпочтения
    prefs = {}
    for line in open(path):
        if line == '"User-ID";"ISBN";"Book-Rating"\n':
            continue
        line = line.replace("\"", "")
        (user, isbn, rating) = line.split(";")
        prefs.setdefault(user, {})
        prefs[user][isbn] = int(rating)
    return prefs

# Визуализация матрицы R


def visualize_R(prefs):
    # из prefs формируем два массива (по x и по y)
    x = []
    y = []
    for user in prefs:
        for book in prefs[user]:
            x.append(int(user))
            y.append(isbnlib.EAN13(book))
    plt.plot(x, y, 'r.')
    plt.show()


# пример реализации функции близости (евклидово расстояние)
def sim_distance_1(prefs, person1, person2):
    # Получить список предметов, оцененных обоими
    # print prefs
    si = {}
    # Если person1 нет в prefs, то вернуть 0
    # if person1 not in prefs:
    #    print 'aaa'
    #    return 0

    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    # Если нет ни одной общей оценки, вернуть 0
    if len(si) == 0:
        return 0

    # сложить квадраты разностей
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sum_of_squares)


# пример реализации функции близости (коэфициент Жаккара)
def sim_distance_2(prefs, person1, person2):
    # Получить список предметов, оцененных обоими
    # print prefs
    si = {}
    # Если person1 нет в prefs, то вернуть 0
    # if person1 not in prefs:
    #    print 'aaa'
    #    return 0
    # ищем одинаковые элементы
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    # Если нет ни одной общей оценки, вернуть 0
    if len(si) == 0:
        return 0
    # объединение
    num_of_union = float(len(prefs[person1]) + len(prefs[person2]))
    return len(si) / num_of_union


# Возвращает отранжированных k пользователей для объекта object_id
def topMatches(prefs_learn_data, person, object_id, k=5, similarity=sim_distance_1):
    # Выбираем только тех пользователей, которые оценили object_id
    prefs_with_object_id = {}
    for user in prefs_learn_data:
        if object_id in prefs_learn_data[user]:
            prefs_with_object_id[user] = prefs_learn_data[user]
    # добавляем самого пользователя, нужен для расчета метрики сходства
    prefs_with_object_id[person] = prefs_learn_data[person]
    # получаем список оценок (с собой не сравниваем!)
    # Формат (мера близости, реальная оценка, айдишник пользователя)
    scores = [(similarity(prefs_with_object_id, person, other), prefs_learn_data[other][object_id], other)
              for other in prefs_with_object_id if other != person]
    scores.sort()
    scores.reverse()
    # Если есть нулевые или отрицательные значения, то удалить их
    result_scores = [score for score in scores if score[0] > 0]
    return result_scores[0:k]


# Получить неизвестную оценку объекта для пользователя
def get_rating(prefs_learn_data, person, object_id, similarity=sim_distance_1):
    # Получаем наиболее похожих пользователей
    scores = topMatches(prefs_learn_data, person,
                        object_id, similarity=similarity)
    # Если для пользователя не нашлось похожих пользователей (белая ворона),
    # то вернуть 0
    if len(scores) == 0:
        return 0
    # Вычисляем сумму произведений оценок на меру близости
    sum_sim_score = sum(score[0] * score[1] for score in scores)
    # Вычисляем сумму всех мер близости
    sum_sims = sum(score[0] for score in scores)
    # Вычисляем рейтинг
    rating = sum_sim_score / sum_sims
    return rating


# Расчет среднеквадратической ошибки
def calculate_error(rating_real, rating_predict):
    sum = 0
    for i in range(len(rating_real) - 1):
        sum += pow(rating_real[i] - rating_predict[i], 2)
    return sqrt(sum)


def get_learn_data(prefs):
    # 80 %
    start = 0
    end = int(len(prefs) * 0.8)
    result = {}
    i = start
    for user in prefs:
        result.setdefault(user, {})
        if i < end:
            result[user] = prefs.get(user)
        i += 1

    return result


@nottest
def get_test_data(prefs):
    # 20 %
    start = int(len(prefs) * 0.8)
    end = len(prefs)
    result = {}
    i = start
    for user in prefs:
        result.setdefault(user, {})
        if i < end:
            result[user] = prefs.get(user)
        i += 1

    return result

# Тестирование разработанной системы на тестовой выборке


@nottest
def test_data():
    # загружаем обучающую выборку и дальше ее будем использовать для прогноза
    # оценки для тестовой выборки
    data = load_data(path='./data/BX-CSV-Dump/BX-Book-Ratings.csv')
    prefs_learn_data = get_learn_data(data)
    test_prefs = get_test_data(data)

    # визуализируем выборку
    visualize_R(prefs_learn_data)

    # загружаем тестовую выборку
    #test_prefs = load_data(path='./data/ml-100k/u-test.data')
    # прогнозируем рейтинги для тестовой выборки (считаем по обучающей!)
    rating_real = []
    rating_predict = []
    for user in test_prefs:
        for book in test_prefs[user]:
            rating_real.append(test_prefs[user][book])
            rating_predict.append(get_rating(prefs_learn_data, str(
                user), str(book), similarity=sim_distance_1))
    # вычисляем ошибку RMSE
    print(rating_predict)
    print(rating_real)
    print(calculate_error(rating_real, rating_predict))


@SkipTest
class TestISBNLib(object):

    def test_isbnlib(self):
        test_data()


def main():
    t = TestISBNLib()
    t.test_isbnlib()


if __name__ == '__main__':
    main()
