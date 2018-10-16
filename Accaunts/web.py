# -*- coding: utf-8 -*-

import time
import webview
from threading import Thread

class Api(Thread):
    def __init__(self):
        super(Api, self).__init__(target=self._request_server_cycle)
        self.storage = []
        self._game_info = {'round': 0, 'isGameStart': False}
        super().start()

    def add_to_storage(self, elem):  # добавление какой-либо переменной в локальное хранилище
        self.storage.append(elem)
        print(elem)

    def signIn(self, trash=0):  # Функция входа в личный кабинет
        login = self.storage.pop()
        print(login)
        password = self.storage.pop()
        print(login, password)
        result = self.connect.sign_in(login, password)
        print(result)
        time.sleep(1)
        if result.get('error') is None:
            webview.evaluate_js("set_window_office();")
            name = result.get('name', '')
            surname = result.get('family', '')
            webview.evaluate_js("set_office_name('Имя: ' + '%s', 'Фамилия: ' + '%s');" % (name, surname))

    def signUp(self, trash=0):  # Функция регистрации и входа в личный кабинет
        login = self.storage.pop()
        password = self.storage.pop()
        name = self.storage.pop()
        surname = self.storage.pop()

        result = self.connect.sign_up(login, password, name, surname)
        time.sleep(1)
        if result.get('error') is None:
            webview.evaluate_js("set_window_office();")
            webview.evaluate_js("set_office_name('Имя: ' + '%s', 'Фамилия: ' + '%s');" % (name, surname))

    def active_office_button(self, trash=0):  # Функция вызывается, когда начинается игра(кнопка становится видимой)
        webview.evaluate_js("set_button_active();")

    def join_the_game(self, trash=0):   # здесь открывается окно с картой и начинается игра
        webview.evaluate_js("set_window_map();")

    # Функция отправляет на страницу номер текущего раунда
    def set_current_round(self, num):
        webview.evaluate_js("set_round(%s);" % num)

    # Функция устанавливает данные поля у ячейки в таблице-карте
    # Координаты, население, транспортные транзакции, текущая минимальная стоимость, вклад магазинов
    def set_cell_info(self, x, y, population, transport_transactions, current_min_cost, contribution_of_stores):
        webview.evaluate_js("""
                            set_cell_info(%s, %s, %s, %s, %s, %s);
                            """ % (x, y, population, transport_transactions, current_min_cost, contribution_of_stores))

    # Функция заполняет всю игровую таблицу
    def fill_table(self, trash=0):
        # TODO получить размеры таблицы
        _x = 0  # TODO получить ширину
        _y = 0  # TODO получить высоту
        for y in range(_y):
            for x in range(_x):
                # TODO Нужно получить эти данные с сервера, наверное
                population = "get"
                transport_transactions = "get"
                current_min_cost = "get"
                contribution_of_stores = "get"
                # заполняем ечейку
                self.set_cell_info(x, y, population, transport_transactions, current_min_cost, contribution_of_stores)

    # Функция устанавливает данные об игроках
    def set_player_info(self, number_id, firstname, lastname, gain):
        webview.evaluate_js("""
                            set_player_info(%s, %s, %s, %s);
                            """ % (number_id, firstname, lastname, gain))

    # Функция заполняет таблицу игроков
    def fill_players(self, trash=0):
        users = self.connect.get_score_sellers().get('value') or []
        for user in users:
            number_id = user['name']
            firstname = user['profit']
            # TODO
            lastname = "get"
            gain = "get"
            # заполняем ечейку
            self.set_player_info(number_id, firstname, lastname, gain)

    #  Функция установки магазина в ячейке
    def set_store(self, trash=0):
        # 6)add_coordinate(координата_x, координата_y, цена(не обязательно)), возвращает  {'value': получилось_ли}
        # вернет нет  если  тебя нет в игре, игра еще не началась или ты на этом раунде уже  ставил магазин
        x = self.storage.pop()
        y = self.storage.pop()
        cost = self.storage.pop()
        print(x, y, cost)
        result = self.connect.add_coordinate(x, y, cost)
        if result.get('value'):
            webview.evaluate_js("""set_store(%s, %s""" % (x, y))    # TODO set_store func js
        else:
            # TODO вывести сообщение "если  тебя нет в игре, игра еще не началась или ты на этом раунде уже  ставил магазин"
            pass

    def _request_server_cycle(self):
        while():
            if self._game_info['isGameStart'] == False:     # Ну, типа if not...
                is_start_game = self.connect.game_is_work()['value']
                self._game_info['isGameStart'] = is_start_game
                if is_start_game:
                    self.active_office_button()
            else:
                round = self.connect.get_index()['value']
                if round != self._game_info['round']:
                    self._game_info['round'] = round
                    self.set_current_round(round)
            time.sleep(5)


if __name__ == '__main__':
    api = Api()
    webview.create_window('Economic game', 'C:/Users/minot/Desktop/Economika/all.html', js_api=api, resizable=True, fullscreen=False,
                          min_size=(600, 450), confirm_quit=False, debug=True)
    # TODO вызвать save on server
