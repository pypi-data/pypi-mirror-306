class UserManager:
    def __init__(self):
        # Инициализация атрибута — словаря для хранения учётных записей.
        self.users_dict = {}

    def add_user(self, user_id, user_data):
        # Логика создания учётной записи.
        if user_id not in self.users_dict:
            self.users_dict[user_id] = user_data
            print(f"Клиент с ID {user_id} добавлен")
        else:
            print(f"Клиент с ID {user_id} уже существует")

    def remove_user(self, user_id):
        # Логика удаления учётной записи.
        if user_id in self.users_dict:
            del self.users_dict[user_id]
            print(f'Клиент с ID {user_id} удалён')
        else:
            print(f'Клиент с ID {user_id} не найден')

    def update_user(self, user_id, user_data):
        # Логика обновления данных клиента.
        if user_id in self.users_dict:
            for key, value in user_data.items():
                self.users_dict[user_id][key] = value
            print(f"Данные клиента с ID {user_id} обновлены")
        else:
            print(f"Клиент с ID {user_id} не найден")

    def find_user(self, user_id):
        # Логика поиска учётной записи.
        if user_id in self.users_dict:
            return self.users_dict[user_id]  # Возвращаем данные клиента
        else:
            print(f"Клиент с ID {user_id} не найден")
            return None  # Возвращаем None, если клиент не найден