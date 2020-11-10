#LAPTOP-D1QCTRIA

import pyodbc
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-D1QCTRIA;'
                      'Database=Practice;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
def isPoint(c):
    return (c == '.' or c== '/' or c == '-')

def isDate(s):
    if len(s) == 10:
        s1 = s[:2]+s[3:5]+s[6:]
        s2 = s[:4]+s[5:7]+s[8:]
        i = 0
        try:
            i = int(s1)
            if isPoint(s[2]) and isPoint(s[5]):
                return True
        except ValueError:
            try:
                i = int(s2)
                if isPoint(s[4]) and isPoint(s[7]):
                    return True
            except ValueError:
                return False

def insert(type):
    str = 'INSERT INTO '
    if type == 1:
        str = str + 'Practice.dbo.Contracts(Customer, ConclDate, ProductKey, GuaranteePeriod, Cost) VALUES (?, ?, ?, ?, ?)'
        print('Последовательно введите значения: Покупатель, Дата заключения договора, Ключ продукции, Период гарантии (дн), Стоимость (₽)')
        params = []
        for i in range (0, 5):
            params.append(input())
        return str, params
    elif type == 2:
        str = str + 'Practice.dbo.Products(ProductID, ProductName) VALUES (?, ?)'
        print(
            'Последовательно введите значения: Идентификатор машины, Название машины')
        params = []
        for i in range(0, 2):
            params.append(input())
        return str, params
    elif type == 3:
        str = str + 'Practice.dbo.Units(UnitCode, UnitName, IsProvided, providerName) VALUES (?, ?, ?, ?)'
        print(
            'Последовательно введите значения: Код узла, Название узла, Закупается ли узел (1 - да, 0 - нет), Название поставщика (- если нет)')
        params = []
        for i in range(0, 4):
            params.append(input())
        return str, params
    elif type == 4:
        str = str + 'Practice.dbo.Complects(ProductId, UnitCode, UnitAmt) VALUES (?, ?, ?)'
        print('Последовательно введите значения: Идентификатор машины, Код узла, Количество узлов в машине')
        params = []
        for i in range(0, 3):
            params.append(input())
        return str, params

def search(type):##########################################################################################
    s = 'SELECT * FROM Practice.dbo.'
    if type == 1:
        s = s + 'Contracts '
        print('Введите номер контракта, Имя заказчика или дату заключения контракта')
        param = input()
        try:
            i = int(param)
            s = s + 'WHERE Id=' + param
        except ValueError:
            if isDate(param):
                s = s + 'WHERE ConclDate=\'' + param + '\''
            else:
                s = s + 'WHERE Customer=\'' + param + '\''
        return s
    elif type == 2:
        s = s + 'Products '
        print('Введите идентификатор или название машины')
        param = input()
        s = s + 'WHERE ProductID=\'' + param + '\' OR ProductName=\'' + param +'\''
        return s
    elif type == 3:
        s = s + 'Units '
        print('Введите код или название узла')
        param = input()
        s = s + 'WHERE UnitCode=\'' + param + '\' OR UnitName=\'' + param +'\''
        return s
    elif type == 4:
        s = s + 'Complects '
        print('Введите идентификатор или машины или узла')
        param = input()
        s = s + 'WHERE ProductID=\'' + param + '\' OR UnitCode=\'' + param +'\''
        return s

def update(type):
    s = 'UPDATE '
    if type == 1:
        s = s + 'Contracts '
        print('Последовательно введите значения: Покупатель, Дата заключения договора, Ключ продукции')
        params = []
        for i in range(0, 3):
            params.append(input())
        params.reverse()
        print('Введите номер столбца, который хотите изменить: 1) Дата изготовления 2) Гарантийный период 3) Дата продажи 4) Стоимость')
        column = input()
        print('Введите новое значение')
        params.append(input())
        params.reverse()
        if column == '1':
            s = s + 'SET MakingDate = ? '
        elif column == '2':
            s = s + 'SET GuaranteePeriod = ? '
        elif column == '3':
            s = s + 'SET SaleDate = ? '
        elif column == '4':
            s = s + 'SET Cost = ? '
        s = s + 'WHERE Customer = ? AND ConclDate = ? AND ProductKey = ?'
        return s, params
    elif type == 2:
        s = s + 'Products '
        print('Введите идентификатор')
        params = []
        params.append(input())
        print('Введите новое название машины')
        params.append(input())
        params.reverse()
        s = s + 'SET ProductName = ? WHERE ProductID = ?'
        return s, params
    elif type == 3:
        s = s + 'Units '
        print('Введите код узла')
        params = []
        params.append(input())
        print('Введите номер столбца, который хотите изменить: 1) Название 2) Поставщик')
        column = input()
        print('Введите новое значение')
        params.append(input())
        params.reverse()
        if column == '1':
            s = s + 'SET UnitName = ? '
        elif column == '2':
            s = s + 'SET ProviderName = ? '
        s = s + 'WHERE UnitCode = ?'
        return s, params
    elif type == 4:
        s = s + 'Complects '
        print('Введите идентификатор машины и узла')
        params = []
        for i in range(0, 2):
            params.append(input())
        print('Введите новое количество соответствующих узлов')
        params.append(input())
        params.reverse()
        s = s + 'SET UnitAmt = ? WHERE UnitCode = ? AND ProductID = ?'
        return s, params

def delete(type):
    s = 'DELETE '
    if type == 1:
        s = s + 'FROM Contracts '
        print('Последовательно введите значения: Покупатель, Дата заключения договора, Ключ продукции')
        params = []
        for i in range(0, 3):
            params.append(input())
        s = s + 'WHERE Customer = ? AND ConclDate = ? AND ProductKey = ?'
        return s, params
    elif type == 2:
        s = s + 'FROM Products '
        print('Введите идентификатор')
        param = input()
        s = s + 'WHERE ProductID = ?'
        return s, param
    elif type == 3:
        s = s + 'FROM Units '
        print('Введите код узла')
        param = input()
        s = s + 'WHERE UnitCode = ?'
        return s, param

print('Для работы с программой вводите команды и данные, следуя инструкциям.')
command = ''
while command.lower() != 'stop':
    print('| 1) Ввод данных | 2) Поиск данных | 3) Изменение данных | 4) Удаление строк | 5) Отключение |')
    command = input()
    if command == '1' or command.lower() == 'ввод данных':
        count = 5
        while count > 0:
            print('Выберите, что нужно добавить в базу данных:')
            print('| 1) Заказ | 2) Машина | 3) Узел | 4) Необходимость узла в машине (связь) | 5) Выход в главное меню |')
            command = input()
            if command == '1' or command.lower() == 'заказ':
                s, prm = insert(1)
                print('Добавляем заказ')
                count = 1
            elif command == '2' or command.lower() == 'машина':
                s, prm = insert(2)
                print('Добавляем машину')
                count = 1
            elif command == '3' or command.lower() == 'узел':
                s, prm = insert(3)
                print('Добавляем узел')
                count = 1
            elif command == '4' or command.lower() == 'связь':
                s, prm = insert(4)
                print('Добавляем связь')
                count = 1
            elif command == '5' or command.lower() == 'выход':
                s = ''
                print('Выходим в главное меню')
                count = 1
            count = count - 1
        if s:
            try:
                cursor.execute(s, prm)
                conn.commit()
                print('Переход в главное меню (нажмите Enter чтобы продолжить)')
                input()
            except pyodbc.DataError:
                print('Произошла ошибка, повторите запрос')
    elif command == '2' or command.lower() == 'поиск данных':
        count = 5
        while count > 0:
            print('Выберите, что нужно найти:')
            print('| 1) Заказ | 2) Машина | 3) Узел | 4) Связь Машина-Узел | 5) Выход в главное меню |')
            command = input()
            # os.system('cls')
            if command == '1' or command.lower() == 'заказ':
                s = search(1)
                print('Ищем заказ')
                count = 1
            elif command == '2' or command.lower() == 'машина':
                s = search(2)
                print('Ищем машину')
                count = 1
            elif command == '3' or command.lower() == 'узел':
                s = search(3)
                print('Ищем узел')
                count = 1
            elif command == '4' or command.lower() == 'связь':
                s = search(4)
                print('Ищем связь')
                count = 1
            elif command == '5' or command.lower() == 'выход':
                s = ''
                print('Выходим в главное меню')
                count = 1
            count = count - 1
        if s:
            try:
                cursor.execute(s)
                gotit = False
                for row in cursor:
                    print(row)
                    gotit = True
                if not gotit:
                    print('Ничего не найдено')
                print('\nПереход в главное меню (нажмите Enter чтобы продолжить)')
                input()
            except pyodbc.DataError:
                print('Произошла ошибка, повторите запрос')
    elif command == '3' or command.lower() == 'изменение данных':
        count = 5
        while count > 0:
            print('Выберите, что нужно изменить:')
            print('| 1) Заказ | 2) Машина | 3) Узел | 4) Связь Машина-Узел | 5) Выход в главное меню |')
            command = input()
            if command == '1' or command.lower() == 'заказ':
                s, prm = update(1)
                count = 1
            elif command == '2' or command.lower() == 'машина':
                s, prm = update(2)
                count = 1
            elif command == '3' or command.lower() == 'узел':
                s, prm = update(3)
                count = 1
            elif command == '4' or command.lower() == 'связь':
                s, prm = update(4)
                count = 1
            elif command == '5' or command.lower() == 'выход':
                s = ''
                print('Выходим в главное меню')
                count = 1
            count = count - 1
        if s:
            try:
                cursor.execute(s, prm)
                conn.commit()
                print('Переход в главное меню (нажмите Enter чтобы продолжить)')
                input()
            except pyodbc.DataError:
                print('Произошла ошибка, повторите запрос')
    elif command == '4' or command.lower() == 'удаление строк':
        count = 5
        while count > 0:
            print('Выберите, что нужно удалить:')
            print('| 1) Заказ | 2) Машина | 3) Узел | 4) Выход в главное меню |')
            command = input()
            if command == '1' or command.lower() == 'заказ':
                s, prm = delete(1)
                count = 1
            elif command == '2' or command.lower() == 'машина':
                s, prm = delete(2)
                count = 1
            elif command == '3' or command.lower() == 'узел':
                s, prm = delete(3)
                count = 1
            elif command == '4' or command.lower() == 'выход':
                s = ''
                print('Выходим в главное меню')
                count = 1
            count = count - 1
        if s:
            try:
                cursor.execute(s, prm)
                conn.commit()
                print('Переход в главное меню (нажмите Enter чтобы продолжить)')
                input()
            except pyodbc.DataError:
                print('Произошла ошибка, повторите запрос')
    elif command == '5' or command.lower() == 'отключение':
        print('Завершение работы программы')
        break
    else:
        print("Команда не распознана, повторите попытку")