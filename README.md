-- Создание таблицы "Категории"
CREATE TABLE Категории (
  id SERIAL PRIMARY KEY,
  название VARCHAR NOT NULL
);

insert into Категории (название) values('категория1');
insert into Категории (название) values('категория2');
insert into Категории (название) values('категория3');

-- Создание таблицы "Товары"
CREATE TABLE Товары (
  id SERIAL PRIMARY KEY,
  название VARCHAR NOT NULL,
  цена DECIMAL(10, 2) NOT NULL,
  категория_id INTEGER REFERENCES Категории(id) ON DELETE CASCADE,
  количество INTEGER NOT NULL
);

-- Создание таблицы "Клиенты"
CREATE TABLE Клиенты (
  id SERIAL PRIMARY KEY,
  ФИО VARCHAR NOT NULL,
  адрес VARCHAR NOT NULL,
  телефон VARCHAR(12) NOT NULL
);

-- Создание таблицы "Заказ"
CREATE TABLE Заказ (
  id SERIAL PRIMARY KEY,
  клиент_id INTEGER REFERENCES Клиенты(id) ON DELETE CASCADE,
  дата_заказа DATE NOT null,
  количество INTEGER NOT NULL
);

-- Создание таблицы "Строка_заказазы"
CREATE TABLE Строка_заказа (
  id SERIAL PRIMARY KEY,
  товар_id INTEGER REFERENCES Товары(id) ON DELETE CASCADE,
  заказ_id integer references Заказ(id) ON DELETE CASCADE 
);

-- Создание таблицы "Сотрудники"
CREATE TABLE Сотрудники (
  id SERIAL PRIMARY KEY,
  ФИО VARCHAR NOT NULL,
  должность VARCHAR NOT NULL
);

-- Создание таблицы "Продажи"
CREATE TABLE Продажи (
  id SERIAL PRIMARY KEY,
  заказ_id INTEGER REFERENCES Заказ(id) ON DELETE CASCADE,
  сотрудник_id INTEGER REFERENCES Сотрудники(id) ON DELETE CASCADE,
  дата_продажи DATE NOT NULL,
  сумма DECIMAL(10, 2)
);
