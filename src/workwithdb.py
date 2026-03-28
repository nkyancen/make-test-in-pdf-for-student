#!/usr/bin/env python3

from DBc import UseDatabase

path_to_base = ''

screen_weight = 1920
screen_height = 1080

main_font = 'serif 14'
other_font = 'serif 11'

types_of_problems = {}
type_of_problem = {}


## Добавляем запись в таблицу БД
def insert_to_database(tab: str, ti: tuple, mask: str = '?') -> None:
    with UseDatabase(path_to_base) as curs:
        curs.execute('INSERT INTO ' + tab + ' VALUES (NULL,' + mask + ')', ti)


## Удаляем запись из таблицы БД
def delete_from_database(tab: str, td: tuple) -> None:
    request_to_delete = 'DELETE FROM ' + tab + ' WHERE %s_id = %s' % td

    with UseDatabase(path_to_base) as currentBase:
        currentBase.execute(request_to_delete)


# Изменяем запись в таблице БД
def database_update(tab: str, tu: tuple) -> None:
    sqlu = 'UPDATE ' + tab + ' SET %s = "%s" WHERE %s_id = %s' % tu

    with UseDatabase(path_to_base) as curentBase:
        curentBase.execute(sqlu)


## Выбираем записи из таблицы БД
def out_from_database(tab: str, to: tuple = ()) -> dict:
    dic = {}

    with UseDatabase(path_to_base) as curs:
        if not to:
            sqlo = 'SELECT * FROM ' + tab
        else:
            sqlo = 'SELECT * FROM ' + tab + ' WHERE %s' % to

        for row in curs.execute(sqlo):
            temp = []

            for i in range(1, len(row)):
                temp.append(str(row[i]))

            dic[str(row[0])] = temp

    return dic


## Возвращаем ключ по значению
def kval(dic: dict, val: list) -> str:
    val = list(val)
    temp = ''
    for item in dic:
        if val == dic[item]:
            temp = item
    return temp


## Проверка зависимости между родительской и дочерней таблицами
def find_couple(dic_child: dict, val_par: str) -> bool:
    temp = []
    for item in dic_child.values():
        temp.append(val_par in item)

    return True in temp


## Проверка наличия пункта в таблице
def find(dic: dict, val: list) -> bool:
    val = list(val)
    temp = []
    for item in dic.values():
        temp.append(val == item)

    return True in temp


## Заменяем номер на текст
def trans(numb, n) -> str:
    numb = int(numb)
    name = str(numb)

    name.rjust(n, "0")

    name = name.replace('0', 'zero')
    name = name.replace('1', 'one')
    name = name.replace('2', 'two')
    name = name.replace('3', 'three')
    name = name.replace('4', 'four')
    name = name.replace('5', 'five')
    name = name.replace('6', 'six')
    name = name.replace('7', 'seven')
    name = name.replace('8', 'eight')
    name = name.replace('9', 'nine')
    return name
