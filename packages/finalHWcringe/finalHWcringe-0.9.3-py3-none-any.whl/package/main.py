from user_management import UserManager
from order_management import OrderManager

user_manager = UserManager()
order_manager = OrderManager()


def main_menu():
    while True:
        print('\nВыберите действие:')
        print('1. Управление учётными записями')
        print('2. Управление заказами')
        print('3. Выход')

        choice = input('Введите номер действия: ')

        if choice == '1':
            user_menu()
        elif choice == '2':
            order_menu()
        elif choice == '3':
            print('Работа завершена.')
            break
        else:
            print('Некорректный ввод. Попробуйте снова.')


def user_menu():
    print('\nУправление учётными записями клиентов:')
    print('1. Добавить учётную запись')
    print('2. Найти учётную запись')
    print('3. Удалить учётную запись')
    print('4. Назад')

    choice = input('Выберите действие: ')

    if choice == '1':
        user_id = input('Введите email клиента: ')
        name = input('Введите имя: ')
        age = int(input('Введите возраст: '))
        user_data = {"name": name, "age": age}
        user_manager.add_user(user_id, user_data)  # Вызов метода создания учётной записи клиента
    elif choice == '2':
        user_id = input('Введите email клиента: ')
        user_info = user_manager.find_user(user_id)  # Вызов метода поиска учётной записи клиента
        if user_info:
            print(f'Данные клиента: {user_info}')
    elif choice == '3':
        user_id = input('Введите email клиента: ')
        user_manager.remove_user(user_id)  # Вызов метода удаления учётной записи клиента
    elif choice == '4':
        return
    else:
        print('Некорректный ввод.')


def order_menu():
    print('\nУправление заказами:')
    print('1. Создать заказ')
    print('2. Обновить заказ')
    print('3. Отменить заказ')
    print('4. Назад')

    choice = input('Выберите действие: ')

    if choice == '1':
        order_id = input('Введите ID заказа: ')
        user_id = input('Введите учётную запись клиента (email): ')

        # Проверяем, существует ли клиент
        if user_manager.find_user(user_id):
            item = input('Введите товар: ')
            price = float(input('Введите цену: '))
            order_data = {"user_id": user_id, "item": item, "price": price}
            order_manager.create_order(order_id, order_data)  # Вызов метода создания заказа
        else:
            print(f'Клиент с ID {user_id} не найден.')

    elif choice == '2':
        order_id = input('Введите ID заказа: ')
        new_data = input('Введите новые данные заказа (в формате "item,price"): ').split(',')

        if len(new_data) == 2:
            item, price = new_data[0], float(new_data[1])
            order_manager.update_order(order_id, {"item": item, "price": price})  # Вызов метода обновления заказа
        else:
            print("Некорректный формат данных.")

    elif choice == '3':
        order_id = input('Введите ID заказа: ')
        order_manager.cancel_order(order_id)  # Вызов метода отмены заказа
    elif choice == '4':
        return
    else:
        print('Некорректный ввод.')


if __name__ == '__main__':
    main_menu()