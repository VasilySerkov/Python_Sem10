def view_data(data, title):
    print(f'{title} = {data}')

def get_value():
    return int(input('Введите число 1: ')), int(input('Введите число 2: '))

def show_menu() -> int:
    print('\n' + '='*20)
    print('1 - Ввести переменные')
    print('2 - Сложение')
    print('3 - Вычитание')
    print('4 - Умножение')
    print('5 - Деление')
    print('6 - Закрыть калькулятор')
    return int(input('Выберите операцию: '))