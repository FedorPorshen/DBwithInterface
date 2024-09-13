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

    def insert_koncpr(self, NAME_PROJECT, JANR, GIT, ID_SOTR):
        query = f"INSERT INTO {self.schema}.koncpr (name_konc, janr_id, git, sotr_id) VALUES (%s, %s, %s, %s) RETURNING *"
        params = (NAME_PROJECT, JANR, GIT, ID_SOTR)
        self.execute_query(query, params)
        self.connection.commit()

    def insert_project(self, NAME_PROJECT, GIT, ID_SOTR, ID_KONCEPT):
        query = f"INSERT INTO {self.schema}.project (name_project, git, sotr_id, koncpr_id) VALUES (%s, %s, %s, %s) RETURNING *"
        params = (NAME_PROJECT, GIT, ID_SOTR, ID_KONCEPT)
        self.execute_query(query, params)
        self.connection.commit()

    def get_table_data(self, table_name):
        if table_name == 'Концепты проектов':
            query = f"SELECT * FROM {self.schema}.koncpr"
            result = self.execute_query(query)
            head = ['id', 'название', 'жанр', 'git', 'сотрудник', 'прошлый концепт']
            return result, head
        elif table_name == 'Готовые проекты':
            query = f"SELECT * FROM {self.schema}.project"
            result = self.execute_query(query)
            head = ['id', 'название', 'git', 'сотрудник', 'прошлый концепт']
            return result, head

    def delete_project_by_id(self, project_id):
        query = f"DELETE FROM {self.schema}.project WHERE id = %s RETURNING *"
        params = (project_id)
        self.execute_query(query, params)
        self.connection.commit()

    def delete_koncept_by_id(self, project_id):
        query = f"DELETE FROM {self.schema}.koncpr WHERE id = %s RETURNING *"
        params = (project_id)
        self.execute_query(query, params)
        self.connection.commit()

    def get_janri(self):
        return self.execute_query(f"SELECT * FROM {self.schema}.janri")

    def get_sotr(self):
        return self.execute_query(f"SELECT * FROM {self.schema}.sotr")

    def get_koncept(self):
        return self.execute_query(f"SELECT * FROM {self.schema}.koncpr")

    def get_project(self):
        return self.execute_query(f"SELECT * FROM {self.schema}.project")

    #def execute_query_many(self, query, params):
     #   cursor = self.connection.cursor()
      #  cursor.executemany(query, params)
       # cursor.close()

class GUI:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def start(self):
        layout_main = [
            [sg.Button('Добавить концепт')],
            [sg.Button('Добавить проект')],
            [sg.Button('Удалить концепт')],
            [sg.Button('Удалить проект')],
            [sg.Button('Посмотреть добавленные проекты')]
        ]

        window_main = sg.Window('Главное окно', layout_main)

        while True:
            event, _ = window_main.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Добавить концепт':

                janr = self.db_connector.get_janri()
                sotr = self.db_connector.get_sotr()

                layout_add = [
                    [sg.Text('Имя проекта:'), sg.Input(key='-NAME_PROJECT-')],
                    [sg.Text('Жанр:'), sg.Combo(janr, key='-JANR-', size=(30, 6), default_value=janr[0])],
                    [sg.Text('Git(ссылки только на гит хаб):'), sg.Input(key='-GIT-')],
                    [sg.Text('Ответственный сотрудник:'), sg.Combo(sotr, size=(30, 6), default_value=sotr[0],key='-ID_SOTR-')],
                    [sg.Button('Добавить'), sg.Button('Отмена')]
                ]

                window_add = sg.Window('Добавить проект', layout_add)

                while True:
                    event, values = window_add.read()
                    if event == sg.WINDOW_CLOSED or event == 'Отмена':
                        break
                    elif event == 'Добавить':
                        NAME_PROJECT = values['-NAME_PROJECT-']
                        JANR = values['-JANR-']
                        JANR = JANR[0]
                        GIT = values['-GIT-']
                        ID_SOTR = values['-ID_SOTR-']
                        ID_SOTR = ID_SOTR[0]
                        #https://github.com/FedorPorshen
                        if GIT[0:19] != 'https://github.com/':
                            sg.popup('неправильно введена ссылка на гит, вводи заново')
                            break
                        self.db_connector.insert_koncpr(NAME_PROJECT, JANR, GIT, ID_SOTR)
                        sg.popup('Проект успешно добавлен!')
                        break

                window_add.close()

            elif event == 'Добавить проект':

                janr = self.db_connector.get_koncept()
                sotr = self.db_connector.get_sotr()

                layout_add = [
                    [sg.Text('Имя проекта:'), sg.Input(key='-NAME_PROJECT-')],
                    [sg.Text('Концепт проекта:'), sg.Combo(janr, size=(30, 6), default_value=janr[0],key='-JANR-')],
                    [sg.Text('Git(ссылки только на гит хаб):'), sg.Input(key='-GIT-')],
                    [sg.Text('Ответственный сотрудник:'), sg.Combo(sotr, size=(30, 6), default_value=sotr[0],key='-ID_SOTR-')],
                    [sg.Button('Добавить'), sg.Button('Отмена')]
                ]

                window_add = sg.Window('Добавить проект', layout_add)

                while True:
                    event, values = window_add.read()
                    if event == sg.WINDOW_CLOSED or event == 'Отмена':
                        break
                    elif event == 'Добавить':
                        NAME_PROJECT = values['-NAME_PROJECT-']
                        JANR = values['-JANR-']
                        JANR = JANR[0]
                        GIT = values['-GIT-']
                        ID_SOTR = values['-ID_SOTR-']
                        ID_SOTR = ID_SOTR[0]
                        #https://github.com/FedorPorshen
                        if GIT[0:19] != 'https://github.com/':
                            sg.popup('неправильно введена ссылка на гит, вводи заново')
                            break
                        self.db_connector.insert_project(NAME_PROJECT, GIT, ID_SOTR, JANR)
                        sg.popup('Проект успешно добавлен!')
                        break

                window_add.close()

            elif event == 'Удалить концепт':

                project = self.db_connector.get_koncept()
                if project == []:
                    sg.popup('Концепт нет в БД!')
                    window_main.close()
                    self.start()

                layout_delete = [
                    [sg.Text('выберете какой концепт удалить:')],
                    [sg.Combo(project,  size=(30, 6), default_value=project[0], key='-ID_PROJECT-')],
                    [sg.Button('удалить'), sg.Button('Отмена')]
                ]

                window_delete = sg.Window('Удаление проекта', layout_delete)

                while True:
                    event_delete, values = window_delete.read()
                    if event_delete == sg.WINDOW_CLOSED or event_delete == 'Отмена':
                        break
                    elif event_delete == 'удалить':
                        project_id = values['-ID_PROJECT-']
                        project_id = str(project_id[0])
                        self.db_connector.delete_koncept_by_id(project_id)
                        sg.popup('Концепт успешно удален!')
                        break

                window_delete.close()

            elif event == 'Удалить проект':

                project = self.db_connector.get_project()

                layout_delete = [
                    [sg.Text('выберете какой проект удалить:')],
                    [sg.Combo(project,  size=(30, 6), default_value=project[0], key='-ID_PROJECT-')],
                    [sg.Button('удалить'), sg.Button('Отмена')]
                ]

                window_delete = sg.Window('Удаление проекта', layout_delete)

                while True:
                    event_delete, values = window_delete.read()
                    if event_delete == sg.WINDOW_CLOSED or event_delete == 'Отмена':
                        break
                    elif event_delete == 'удалить':
                        project_id = values['-ID_PROJECT-']
                        project_id = str(project_id[0])
                        self.db_connector.delete_project_by_id(project_id)
                        sg.popup('Проект успешно удален!')
                        break

                window_delete.close()

            elif event == 'Посмотреть добавленные проекты':
                self.view_project()

        window_main.close()

    def view_project(self):
        table_names = [
            'Концепты проектов',
            'Готовые проекты',
        ]

        layout = [
            [sg.Text('Выберите таблицу:')],
            [sg.Listbox(table_names, size=(100, len(table_names)), key='-TABLE_LIST-')],
            [sg.Button('OK')]
        ]

        window = sg.Window('Выбор', layout, size=(400, 300))

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'OK':
                selected_table = values['-TABLE_LIST-'][0]
                table_data, head = self.db_connector.get_table_data(selected_table)
                self.view_project2(table_data, head)
                break

        window.close()

    def view_project2(self, val, head):
        layout = [
            [sg.Table(values=val, headings=head, size=(200,100))],
            [sg.Button('OK')],
        ]

        window = sg.Window('Выбор таблицы', layout, size=(500, 300))

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'OK':
                break

        window.close()

if __name__ == '__main__':
    db_connector = DatabaseConnector(schema='kyrs')
    gui = GUI(db_connector)
    gui.start()