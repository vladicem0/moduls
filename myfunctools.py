from datetime import datetime
from functools import wraps


_func_list = {}
_start = None
_stop = None
_cur_time = []


class FuncInfo:
    def __init__(self, func_name, time):
        self.func_name = func_name
        self.count = 1
        self.time = [round(time, 3)]
        _func_list[func_name] = self

    def __str__(self):
        output = 'Функция: "' + self.func_name + '"\n'
        output += 'Количество вызовов: ' + str(self.count) + '\n'
        output += 'Время выполения (ms): ' + self.time.__str__() + '\n'
        output += 'Общее время выполнения (ms) ' + str(round(sum(self.time), 3)) + '\n'
        output += 'Среднее время выполнения (ms): ' + str(round(sum(self.time)/self.count, 3)) + '\n'
        return output

    def update_info(self, time):
        self.count += 1
        self.time.append(round(time, 3))

    @classmethod
    def print(cls):
        for instance in _func_list.values():
            print(instance)

    @classmethod
    def get_name(cls, name=None):
        if name is None:
            print('Список вызванных функций:')
            for instance in _func_list.values():
                print(instance.func_name)
            print()
        else:
            try:
                print(_func_list[name].func_name, '\n')
            except KeyError:
                if name in globals().keys():
                    print('Функция не была использована')
                else:
                    print('Введенная функция не существует')

    @classmethod
    def get_count(cls, name=None):
        if name is None:
            print('Количество вызовов функций:')
            for instance in _func_list.values():
                print(f'{instance.func_name}: {instance.count}')
            print()
        else:
            try:
                print(f'Количество вызовов функции "{_func_list[name].func_name}": {_func_list[name].count}\n')
            except KeyError:
                print('Функция не существует или не была использована')

    @classmethod
    def get_time(cls, name=None):
        if name is None:
            print('Время выполнения функций:')
            for instance in _func_list.values():
                print(instance.func_name)
                print(f'Время выполнения (ms): {instance.time.__str__()}')
                print(f'Общее время выполнения (ms): {round(sum(instance.time), 3)}')
                print(f'Среднее время выполнения (ms): {round(sum(instance.time)/instance.count, 3)}\n')
        else:
            try:
                print(f'Время выполнения функции "{_func_list[name].func_name}":')
                print(f'Время выполнения (ms): {_func_list[name].time.__str__()}')
                print(f'Общее время выполнения (ms): {round(sum(_func_list[name].time), 3)}')
                print(f'Среднее время выполнения (ms): {round(sum(_func_list[name].time)/_func_list[name].count, 3)}\n')
            except KeyError:
                print('Функция не существует или не была использована')


def execute_time(function):
    """
    Декоратор для измерения времени выполнения функции
    """
    @wraps(function)
    def wrapper():
        start = datetime.now()
        function()
        end = datetime.now()
        print((end - start).total_seconds()*1000, 'ms', function.__name__)
    return wrapper


def init_info(function):
    """
    Декоратор для добавления функции в класс сборщика информации. Работает только
    для нерекурсивных функций.
    При использовании нескольких декораторов, init_info необходимо поместить непосредственно перед
    оборачиваемой функцией
    """
    def wrapper(*args):
        start = datetime.now()
        function(*args)
        end = datetime.now()
        exe_time = (end - start).total_seconds() * 1000
        func_name = function.__name__
        if func_name in _func_list.keys():
            FuncInfo.update_info(_func_list[func_name], exe_time)
        else:
            FuncInfo(func_name, exe_time)
    return wrapper


def init_info_rec(function):
    """
    Декоратор для добавления рекурсивных функции в класс сборщика информации.
    При использовании нескольких декораторов, init_info_rec необходимо поместить непосредственно перед
    оборачиваемой функцией
    """
    @wraps(function)
    def wrapper(*args):
        global _start, _stop
        if _start is None:
            _start = datetime.now()
        else:
            _cur_time.append((datetime.now() - _start).total_seconds() * 1000)
            _start = datetime.now()
        function(*args)
        if _stop is None:
            exe_time = (datetime.now() - _start).total_seconds() * 1000
        else:
            exe_time = (datetime.now() - _stop).total_seconds() * 1000 + _cur_time[-1]
            _cur_time.pop(-1)
        func_name = function.__name__
        if func_name in _func_list.keys():
            FuncInfo.update_info(_func_list[func_name], exe_time)
        else:
            FuncInfo(func_name, exe_time)
        _stop = datetime.now()
    return wrapper
