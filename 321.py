import psycopg2
import PySimpleGUI as sg


class DatabaseConnector:
    def __init__(self, schema):
        self.connection = psycopg2.connect(
            host='127.0.0.1',
            database='postgres',
            user='postgres',
            password='123'
        )
        self.schema = schema


    def execute_query(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        return result

    def insert_client(self, FIO, address, phone):
        query = f"INSERT INTO {self.schema}.Клиенты (ФИО, адрес, телефон) VALUES (%s, %s, %s) RETURNING *"
        params = (FIO, address, phone)
        self.execute_query(query, params)
        self.connection.commit()

    def insert_employee(self, FIO, position):
        query = f"INSERT INTO {self.schema}.Сотрудники (ФИО, должность) VALUES (%s, %s) RETURNING *"
        params = (FIO, position)
        self.execute_query(query, params)
        self.connection.commit()

    def insert_product(self, name, price, category_id, count):
        query = f"INSERT INTO {self.schema}.Товары (название, цена, категория_id, количество) VALUES (%s, %s, %s, %s) RETURNING *"
        params = (name, price, category_id, count)
        self.execute_query(query, params)
        self.connection.commit()

    def insert_order(self, client_id, date, count, product_ids):
        order_query = f"INSERT INTO {self.schema}.Заказ (клиент_id, дата_заказа, количество) VALUES (%s, %s, %s) RETURNING id"
        order_params = (client_id, date, count)
        order_id = self.execute_query(order_query, order_params)[0][0]

        order_lines_query = f"INSERT INTO {self.schema}.Строка_заказа (заказ_id, товар_id) VALUES (%s, %s)"
        order_lines_params = [(order_id, product_id) for product_id in product_ids]
        self.execute_query_many(order_lines_query, order_lines_params)
        self.connection.commit()

    def insert_sale(self, order_id, employee_id, date):
        query = f"INSERT INTO {self.schema}.Продажи (заказ_id, сотрудник_id, дата_продажи) VALUES (%s, %s, %s) RETURNING *"
        params = (order_id, employee_id, date)
        self.execute_query(query, params)
        self.connection.commit()

    def db_update_client(self, id, upd, qwe):
        query = f"UPDATE {self.schema}.Клиенты SET {upd} = %s where id = %s RETURNING *"
        params = (qwe, id)
        self.execute_query(query, params)
        self.connection.commit()

    def delete_client_by_id(self, client_id):
        query = f"DELETE FROM {self.schema}.Клиенты WHERE id = %s RETURNING *"
        params = (client_id,)
        self.execute_query(query, params)
        self.connection.commit()

    def delete_employee_by_id(self, employee_id):
        query = f"DELETE FROM {self.schema}.Сотрудники WHERE id = %s RETURNING *"
        params = (employee_id,)
        self.execute_query(query, params)
        self.connection.commit()

    def delete_product_by_id(self, product_id):
        query = f"DELETE FROM {self.schema}.Товары WHERE id = %s RETURNING *"
        params = (product_id,)
        self.execute_query(query, params)
        self.connection.commit()

    def get_table_data(self, table_name):
        if table_name == 'Траты клиентов':
            query = f"select ФИО, sum(сумма) from org.Клиенты inner join org.Заказ on Заказ.клиент_id = Клиенты.id INNER JOIN org.Продажи ON org.Продажи.заказ_id = org.Заказ.id group by ФИО;"
            result = self.execute_query(query)
            head = ['Фамилия имя отчество', 'сумма']
            return result, head
        elif table_name == 'Категории':
            query = f"SELECT * FROM {self.schema}.{table_name}"
            result = self.execute_query(query)
            head = ['id','название']
            return result, head
        elif table_name == 'Товары':
            query = f"SELECT * FROM {self.schema}.{table_name}"
            result = self.execute_query(query)
            head = ['id','название', 'цена', 'кат_id', 'кол-во']
            return result, head
        elif table_name == 'Клиенты':
            query = f"SELECT * FROM {self.schema}.{table_name}"
            result = self.execute_query(query)
            head = ['id','ФИО','адрес','телефон']
            return result, head
        elif table_name == 'Заказ':
            query = f"SELECT * FROM {self.schema}.{table_name}"
            result = self.execute_query(query)
            head = ['id','клиент_id','дата заказа','количество']
            return result, head
        elif table_name == 'Строка_заказа':
            query = f"SELECT * FROM {self.schema}.{table_name}"
            result = self.execute_query(query)
            head = ['id','товар_id','заказ_id',]
            return result, head
        elif table_name == 'Сотрудники':
            query = f"SELECT * FROM {self.schema}.{table_name}"
            result = self.execute_query(query)
            head = ['id','ФИО','должность']
            return result, head
        elif table_name == 'Продажи':
            query = f"SELECT * FROM {self.schema}.{table_name}"
            result = self.execute_query(query)
            head = ['id','зак_id','сотр_id','дата продажи','сумма']
            return result, head

    def get_products(self):
        return self.execute_query(f"SELECT * FROM {self.schema}.Товары")

    def execute_query_many(self, query, params):
        cursor = self.connection.cursor()
        cursor.executemany(query, params)
        cursor.close()

class GUI:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def add_client(self):
        layout = [
            [sg.Text('ФИО:'), sg.Input(key='-FIO-')],
            [sg.Text('Адрес:'), sg.Input(key='-ADDRESS-')],
            [sg.Text('Телефон:'), sg.Input(key='-PHONE-')],
            [sg.Button('Добавить'), sg.Button('Отмена')]
        ]

        window = sg.Window('Добавить клиента', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Отмена':
                break
            elif event == 'Добавить':
                FIO = values['-FIO-']
                address = values['-ADDRESS-']
                phone = values['-PHONE-']
                self.db_connector.insert_client(FIO, address, phone)
                sg.popup('Клиент успешно добавлен!')
                break

        window.close()

    def add_employee(self):
        layout = [
            [sg.Text('ФИО:'), sg.Input(key='-FIO-')],
            [sg.Text('Должность:'), sg.Input(key='-POSITION-')],
            [sg.Button('Добавить'), sg.Button('Отмена')]
        ]

        window = sg.Window('Добавить сотрудника', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Отмена':
                break
            elif event == 'Добавить':
                FIO = values['-FIO-']
                position = values['-POSITION-']
                self.db_connector.insert_employee(FIO, position)
                sg.popup('Сотрудник успешно добавлен!')
                break

        window.close()

    def add_product(self):
        layout = [
            [sg.Text('Название:'), sg.Input(key='-NAME-')],
            [sg.Text('Цена:'), sg.Input(key='-PRICE-')],
            [sg.Text('Категория ID:'), sg.Input(key='-CATEGORY_ID-')],
            [sg.Text('количество:'), sg.Input(key='-COUNT-')],
            [sg.Button('Добавить'), sg.Button('Отмена')]
        ]

        window = sg.Window('Добавить товар', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Отмена':
                break
            elif event == 'Добавить':
                name = values['-NAME-']
                price = values['-PRICE-']
                category_id = values['-CATEGORY_ID-']
                count = values['-COUNT-']
                self.db_connector.insert_product(name, price, category_id, count)
                sg.popup('Товар успешно добавлен!')
                break

        window.close()

    def create_insert_order_form(self):
        products = self.db_connector.get_products()
        layout = [
            [sg.Text('ID клиента:'), sg.Input(key='client_id')],
            [sg.Text('Дата заказа:'), sg.Input(key='date')],
            [sg.Text('Количество:'), sg.Input(key='count')],
            [sg.Text('Выбранные товары:')],
            [sg.Text('Выберите товары и укажите количество:')],
            [sg.Checkbox(f"{product[1]}", key=f"product_{product[0]}") for product in products],
            [sg.Button('Добавить заказ')]
        ]

        window = sg.Window('Добавление заказа', layout)

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Добавить заказ':
                # Получение выбранных товаров
                product_ids = [int(key.split('_')[1]) for key, value in values.items() if
                               key.startswith('product_') and value]

                # Вызов метода insert_order
                self.db_connector.insert_order(
                    int(values['client_id']),
                    values['date'],
                    int(values['count']),
                    product_ids
                )
                sg.popup('заказ успешно добавлен!')
                break

        window.close()



    def add_sale(self):
        layout = [
            [sg.Text('Id заказа:'), sg.Input(key='-ID_ORDER-')],
            [sg.Text('Id сотрудника:'), sg.Input(key='-ID_EMPLOYEE-')],
            [sg.Text('Дата продажи:'), sg.Input(key='-DATE-')],
            [sg.Button('Добавить'), sg.Button('Отмена')]
        ]

        window = sg.Window('Добавить продажу', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Отмена':
                break
            elif event == 'Добавить':
                id_order = values['-ID_ORDER-']
                id_employee = values['-ID_EMPLOYEE-']
                date = values['-DATE-']
                self.db_connector.insert_sale(id_order, id_employee, date)
                sg.popup('Продажа успешно добавлена!')
                break

        window.close()

    def update_client(self, upd):
        layout = [
            [sg.Text('id:'), sg.Input(key='-ID-')],
            [sg.Text(upd), sg.Input(key='-UPD-')],
            [sg.Button('Изменить')]
        ]

        window = sg.Window('Изменить клиента', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Отмена':
                break
            elif event == 'Изменить':
                id = values['-ID-']
                qwe = values['-UPD-']
                print(id + ' ' + upd)
                self.db_connector.db_update_client(id, upd, qwe)
                sg.popup('Клиент успешно изменен!')
                break

        window.close()

    def delete_client(self):
        layout = [
            [sg.Text('ID клиента:'), sg.Input(key='-CLIENT_ID-')],
            [sg.Button('Удалить'), sg.Button('Отмена')]
        ]

        window = sg.Window('Удалить клиента', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Отмена':
                break
            elif event == 'Удалить':
                client_id = values['-CLIENT_ID-']
                self.db_connector.delete_client_by_id(client_id)
                sg.popup('Клиент успешно удален!')
                break

        window.close()

    def delete_employee(self):
        layout = [
            [sg.Text('ID сотрудника:'), sg.Input(key='-EMPLOYEE_ID-')],
            [sg.Button('Удалить'), sg.Button('Отмена')]
        ]

        window = sg.Window('Удалить сотрудника', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Отмена':
                break
            elif event == 'Удалить':
                employee_id = values['-EMPLOYEE_ID-']
                self.db_connector.delete_employee_by_id(employee_id)
                sg.popup('Сотрудник успешно удален!')
                break

        window.close()

    def delete_product(self):
        layout = [
            [sg.Text('ID товара:'), sg.Input(key='-PRODUCT_ID-')],
            [sg.Button('Удалить'), sg.Button('Отмена')]
        ]

        window = sg.Window('Удалить товар', layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Отмена':
                break
            elif event == 'Удалить':
                product_id = values['-PRODUCT_ID-']
                self.db_connector.delete_product_by_id(product_id)
                sg.popup('Товар успешно удален!')
                break

        window.close()

    def view_table(self):
        table_names = [
            'Категории',
            'Товары',
            'Клиенты',
            'Заказ',
            'Строка_заказа',
            'Сотрудники',
            'Продажи',
            'Траты клиентов',
        ]

        layout = [
            [sg.Text('Выберите таблицу:')],
            [sg.Listbox(table_names, size=(100, len(table_names)), key='-TABLE_LIST-')],
            [sg.Button('OK')]
        ]

        window = sg.Window('Выбор таблицы', layout, size=(400, 300))

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'OK':
                selected_table = values['-TABLE_LIST-'][0]
                table_data, head = self.db_connector.get_table_data(selected_table)
                self.view_table2(table_data, head)
                break

        window.close()


    def view_table2(self, val, head):
        layout = [
            [sg.Table(values=val, headings=head, size=(200,100))],
            [sg.Button('OK')],
        ]

        window = sg.Window('Выбор таблицы', layout, size=(400, 300))

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'OK':
                break

        window.close()

    def run(self):
        layout_main = [
            [sg.Button('Добавить кого-то')],
            [sg.Button('Изменить клиента')],
            [sg.Button('Удалить кого-то')],
            [sg.Button('Посмотреть таблицу')]
        ]

        window_main = sg.Window('Главное окно', layout_main)

        while True:
            event, _ = window_main.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Добавить кого-то':
                layout_add = [
                    [sg.Button('Клиент')],
                    [sg.Button('Сотрудник')],
                    [sg.Button('Товар')],
                    [sg.Button('Заказы')],
                    [sg.Button('Продажи')],
                ]

                window_add = sg.Window('Добавить кого-то', layout_add)

                while True:
                    event_add, _ = window_add.read()
                    if event_add == sg.WINDOW_CLOSED:
                        break
                    elif event_add == 'Клиент':
                        self.add_client()
                        break
                    elif event_add == 'Сотрудник':
                        self.add_employee()
                        break
                    elif event_add == 'Товар':
                        self.add_product()
                        break
                    elif event_add == 'Заказы':
                        self.create_insert_order_form()
                        break
                    elif event_add == 'Продажи':
                        self.add_sale()
                        break

                window_add.close()

            elif event == 'Изменить клиента':
                layout_upd = [
                    [sg.Button('ФИО')],
                    [sg.Button('адрес')],
                    [sg.Button('телефон')],
                ]

                window_upd = sg.Window('Изменить клиента', layout_upd)

                while True:
                    event_add, _ = window_upd.read()
                    if event_add == sg.WINDOW_CLOSED:
                        break
                    elif event_add == 'ФИО':
                        self.update_client('ФИО')
                        break
                    elif event_add == 'адрес':
                        self.update_client('адрес')
                        break
                    elif event_add == 'телефон':
                        self.update_client('телефон')
                        break

                window_upd.close()

            elif event == 'Удалить кого-то':
                layout_delete = [
                    [sg.Button('Клиент')],
                    [sg.Button('Сотрудник')],
                    [sg.Button('Товар')],
                ]

                window_delete = sg.Window('Удалить кого-то', layout_delete)

                while True:
                    event_delete, _ = window_delete.read()
                    if event_delete == sg.WINDOW_CLOSED:
                        break
                    elif event_delete == 'Клиент':
                        self.delete_client()
                        break
                    elif event_delete == 'Сотрудник':
                        self.delete_employee()
                        break
                    elif event_delete == 'Товар':
                        self.delete_product()
                        break

                window_delete.close()

            elif event == 'Посмотреть таблицу':
                self.view_table()

        window_main.close()


if __name__ == '__main__':
    db_connector = DatabaseConnector(schema='org')
    gui = GUI(db_connector)
    gui.run()