import string
import unittest
from abc import abstractmethod
from Accaunts import Accaunt
import webview


def starter() -> int:
    # TODO Релизовать начальный экран и кнопки.
    # mainlook и кнопка для входа (Администратор и преподователи)
    return 1


def _sign_in() -> int:
    # TODO Релизовать вход.
    # Вернет уровень доступа в случае успеха, осуществляет сввязь с БД. TODO Подумать о безопасности.
    pass


def _register_(login, password) -> int:
    # Регистрировать может только администратор. (С 3 уровнем доступа)
    current_acc = Accaunt.Account()
    current_acc.login = login
    current_acc._password = password
    add_accaunt_to_base(current_acc)
    return current_acc.get_lvl()


def add_accaunt_to_base(acc) -> bool:
    # TODO Релизовать добавления аакаунта в базу.
    #  Должна вернуть True или False в зависимости от результата (Успех - True | Ошибка - False).
    pass


def main_look() -> Accaunt:
    # TODO Релизовать Просмотр расписания.
    pass


def make_model() -> Accaunt:
    # TODO Релизовать систему создания базовой модели расписания.
    pass


def add_comments() -> str:
    # TODO Релизовать добавление комментариев от преподаователей.
    pass


# class TestSystem(unittest.TestCase):
#     # TODO Релизовать UnitTests, подумать о других тестах.
#     def test_one(self):
#         result = 1
#         self.assertEqual(starter(), result)


class Api:
    def __init__(self):
        self.storage = []

    def add_to_storage(self, elem):
        self.storage.append(elem)

    def signIn(self, trash=0):
        webview.evaluate_js("""set_window_menu();""")


if __name__ == '__main__':
    # unittest.main()
    api = Api()
    webview.create_window('Shedule', './all.html', js_api=api, resizable=True,
                          fullscreen=False,
                          min_size=(600, 450), confirm_quit=False, debug=True)
