class OrderManager:
    def __init__(self):
        # Инициализация атрибута — словаря для хранения заказов.
        self.orders_dict = {}

    def create_order(self, order_id, order_data):
        # Логика создания заказа.
        if order_id not in self.orders_dict:
            self.orders_dict[order_id] = order_data
            print(f'Заказ с ID {order_id} добавлен.')
        else:
            print(f'Заказ с ID {order_id} уже существует.')

    def update_order(self, order_id, order_data):
        # Логика обновления заказа.
        if order_id in self.orders_dict:
            self.orders_dict[order_id] = order_data
            print(f'Заказ с ID {order_id} обновлён.')
        else:
            print(f'Заказ с ID {order_id} не найден.')

    def cancel_order(self, order_id):
        # Логика отмены заказа.
        if order_id in self.orders_dict:
            del self.orders_dict[order_id]
            print(f'Заказ с ID {order_id} отменён.')
        else:
            print(f'Заказ с ID {order_id} не найден.')
