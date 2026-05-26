# Домашнее задание №5: Работа с объектами в ORM

# Содержание

- [Инструкция](#инструкция)
- [Распределение процентов](#распределение-процентов)
- [Общие критерии](#общие-критерии)
- [Условие задачи](#условие-задачи)
  - [1. Создание базы данных и таблиц](#1-создание-базы-данных-и-таблиц)
    - [Таблица books](#таблица-books)
    - [Таблица users](#таблица-users)
    - [Таблица user_book_association](#таблица-user_book_association)
    - [Таблица delivery](#таблица-delivery)
  - [2. Заполнение таблиц данными](#2-заполнение-таблиц-данными)
    - [Книги](#книги)
    - [Пользователи](#пользователи)
    - [Доставка (delivery)](#доставка-delivery)
    - [Ассоциация пользователей и книг](#ассоциация-пользователей-и-книг)
  - [3. Запросы](#3-запросы)
- [Ожидаемый результат](#ожидаемый-результат)
  - [2.1. Добавление книг](#21-добавление-книг)
  - [2.2. Добавление пользователей](#22-добавление-пользователей)
  - [2.3. Добавление данных доставки](#23-добавление-данных-доставки)
  - [2.4. Добавление данных ассоциации](#24-добавление-данных-ассоциации-пользователя-и-книги)
  - [3.1. Топ-3 самые популярные книги](#31-топ-3-самые-популярные-книги)
  - [3.2. Информация о покупках пользователей](#32-информация-о-покупках-пользователей)
  - [3.3. Пользователи с отсутствующими данными доставки](#33-пользователи-с-отсутствующими-данными-доставки)
  - [3.4. Увеличение цены на 5%](#34-увеличение-цены-на-5)
  - [3.5. Отчет по магазину](#35-отчет-по-магазину)
  - [3.6. Удаление пользователей без адреса](#36-удаление-пользователей-без-адреса)
  - [3.7. Удаление книги по ISBN](#37-удаление-книги-по-isbn)

---

## Инструкция

1. 📥 Переключитесь в PyCharm на ветку `main` и обновите её с помощью `Update Project...`
2. 🌿 Создайте новую ветку под названием `hw5`.
3. 💻 Напишите код, необходимый для решения задачи (условие задачи находится во вложении к домашнему заданию).
4. ✨ Выполните автоформатирование кода:
   ```
   uv run ruff format
   uv run ruff check --fix
   ```
   📍Если есть ошибки — исправьте.
5. 🔀 Выполните PR в ветку `main` и добавьте преподавателя в `Reviewers`.

---

📌 В качестве ответа приложите ссылку на PR.

ℹ️ Пример ссылки: `https://github.com/Username/SQLAlchemyCourse/pull/1`

---

## Распределение процентов

➡️ **100 %** — Все задачи выполнены в полном объёме и без замечаний

➡️ **90–99 %** — Выполнены все задачи, но есть мелкие недочеты, которые не влияют на результат. Нет ошибок PEP8.

➡️ **80–89 %** — Выполнены все задачи, но есть недочеты, которые не влияют на результат. Нет ошибок PEP8.

➡️ **75–79 %** — Выполнены все задачи, но есть недочеты, которые частично влияют на результат (максимум 1 некорректный результат). Есть ошибки PEP8 (не более 5 ошибок).

➡️ **Менее 75 %** — Задание не выполнено или выполнено с критическими ошибками.

---

## Общие критерии

### 1. ⚙️ Функциональность.
- Прохождение тестов или проверка с верным ответом.
- Соответствие заданию.
- Отсутствие ошибок исполнения: код не падает с `SyntaxError`, `NameError`, `TypeError` или `AttributeError` при стандартных входных данных.

### 2. 📖 PEP8 (читаемость и стиль).
- Замечания, связанные со стандартом PEP8 (например, избыточное количество пробелов, отступов или символов в строке, некорректные названия переменных).
- Проверяется при помощи `uv run ruff check`.

### 3. 🧠 Логика и структура.
- Соблюдение принципов разработки кода:
  - **YAGNI** (You Aren’t Gonna Need It): не пишите код, если думаете, что он пригодится позже.
  - **DRY** (Don’t Repeat Yourself): не дублируйте код.
  - **KISS** (Keep It Simple, Stupid): не придумывайте к задаче более сложного решения, чем ей требуется.

### 4. 🛡️ Безопасность и надёжность.
- Предварительная проверка.
- Обработка исключений.
- Закрытие ресурсов.

### 5. 📚 Документация, аннотации и комментарии.
- Docstring для каждой функции и класса.
- Использование аннотаций в функциях, методах и переменных.
- Отсутствие закомментированного кода.
- Комментарии объясняют **ПОЧЕМУ** код написан так, а не **ЧТО** он делает (что должно быть очевидно из кода).

---

## Условие задачи

> Книжный магазин

### 1. Создание базы данных и таблиц

Создайте базу данных `bookstore.db`

#### Таблица `books`

| Поле    | Тип      | Ограничения                   | Описание                          |
|---------|----------|-------------------------------|-----------------------------------|
| id      | INTEGER  | PRIMARY KEY AUTOINCREMENT     | Уникальный идентификатор          |
| title   | STRING   | NOT NULL                      | Название книги                    |
| author  | STRING   | NOT NULL                      | Автор книги                       |
| year    | INTEGER  |                               | Год издания                       |
| isbn    | STRING   | UNIQUE                        | ISBN книги                        |
| pages   | INTEGER  | DEFAULT 0                     | Количество страниц                |
| genre   | STRING   |                               | Жанр                              |
| count   | INTEGER  | DEFAULT 1                     | Количество                        |
| price   | FLOAT    | NOT NULL, DEFAULT 0           | Цена                              |

**Атрибуты:**
- `users` — `LIST[UserBookAssociation]` (список пользователей книги, связь многие-ко-многим)

**Свойства:**
- `is_available` — доступность книги (`True`, если `count > 0`)
- `list_users` — список пользователей, у которых есть книга, в формате `f'{user.id}: {user.fullname} ({user.name})'`

Проверьте, что таблица создалась.

---

#### Таблица `users`

| Поле     | Тип          | Ограничения               | Описание              |
|----------|--------------|---------------------------|-----------------------|
| id       | INTEGER      | PRIMARY KEY AUTOINCREMENT | Уникальный идентификатор |
| name     | STRING(30)   | NOT NULL, UNIQUE          | Ник пользователя      |
| fullname | STRING(50)   |                           | ФИО пользователя      |

**Атрибуты:**
- `books` — `LIST[UserBookAssociation]` (список книг пользователя, связь многие-ко-многим)
- `delivery_info` — `LIST[Delivery]` (список данных доставки, связь один-ко-многим)

**Свойства:**
- `is_books` — есть ли книги у пользователя (`True/False`)
- `list_books` — список книг пользователя в формате `f'{book.id}: {book.title} ({book.author})'`

Проверьте, что таблица создалась.

---

#### Таблица `user_book_association`

| Поле    | Тип     | Ограничения                            | Описание                    |
|---------|---------|----------------------------------------|-----------------------------|
| user_id | INTEGER | PRIMARY KEY, FOREIGN KEY (users.id)    | ID пользователя             |
| book_id | INTEGER | PRIMARY KEY, FOREIGN KEY (books.id)    | ID книги                    |

**Атрибуты:**
- `user` — `User` (связь с атрибутом `books`)
- `book` — `Book` (связь с атрибутом `users`)

Проверьте, что таблица создалась.

---

#### Таблица `delivery`

| Поле     | Тип         | Ограничения               | Описание                    |
|----------|-------------|---------------------------|-----------------------------|
| id       | INTEGER     | PRIMARY KEY AUTOINCREMENT | Уникальный идентификатор    |
| user_id  | INTEGER     | FOREIGN KEY               | ID пользователя             |
| email    | STRING(50)  | UNIQUE                    | Почта пользователя          |
| address  | STRING      |                           | Адрес пользователя          |
| phone    | STRING(15)  | UNIQUE                    | Телефон пользователя        |

**Атрибуты:**
- `user` — объект пользователя (связь многие-к-одному)

Проверьте, что таблица создалась.

---

### 2. Заполнение таблиц данными

#### Книги

Добавьте в таблицу `books` следующие книги:

```python
[
    {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "year": 1967, "isbn": "978-5-17-135043-1", "pages": 480, "genre": "Роман", "count": 5, "price": 890.0},
    {"title": "Преступление и наказание", "author": "Федор Достоевский", "year": 1866, "isbn": "978-5-04-116633-9", "pages": 672, "genre": "Роман", "count": 3, "price": 750.0},
    {"title": "1984", "author": "Джордж Оруэлл", "year": 1949, "isbn": "978-5-17-137262-4", "pages": 320, "genre": "Антиутопия", "count": 2, "price": 650.0},
    {"title": "Убить пересмешника", "author": "Харпер Ли", "year": 1960, "isbn": "978-5-04-116631-5", "pages": 416, "genre": "Роман", "count": 0, "price": 550.0},
    {"title": "Война и мир. Том 1", "author": "Лев Толстой", "year": 1867, "isbn": "978-5-17-135042-4", "pages": 720, "genre": "Роман-эпопея", "count": 1, "price": 1200.0},
    {"title": "Анна Каренина", "author": "Лев Толстой", "year": 1877, "isbn": "978-5-04-116632-2", "pages": 864, "genre": "Роман", "count": 0, "price": 950.0},
    {"title": "Собачье сердце", "author": "Михаил Булгаков", "year": 1925, "isbn": "978-5-17-135044-8", "pages": 352, "genre": "Повесть", "count": 4, "price": 590.0},
    {"title": "Маленький принц", "author": "Антуан де Сент-Экзюпери", "year": 1943, "isbn": "978-5-04-116634-6", "pages": 96, "genre": "Сказка", "count": 7, "price": 450.0},
    {"title": "Три товарища", "author": "Эрих Мария Ремарк", "year": 1936, "isbn": "978-5-17-137263-1", "pages": 384, "genre": "Роман", "count": 2, "price": 690.0},
    {"title": "Портрет Дориана Грея", "author": "Оскар Уайльд", "year": 1890, "isbn": "978-5-04-116635-3", "pages": 320, "genre": "Роман", "count": 0, "price": 520.0}
]
```

**Требования:**
- Используйте `session.add_all(list_books)`.
- Получите `id` книг с помощью `flush()`.
- Выведите количество добавленных книг (длина списка `id`).

---

#### Пользователи

Добавьте в таблицу `users`:

```python
[
    {"name": "alice", "fullname": "Alice Wonderland"},
    {"name": "bob", "fullname": "Bob Builder"},
    {"name": "charlie", "fullname": "Charlie Brown"},
    {"name": "diana", "fullname": "Diana Princess"},
    {"name": "eve", "fullname": "Eve Smith"},
]
```

**Требования:**
- Используйте `session.add_all()`.
- Выведите количество добавленных пользователей.

---

#### Доставка (delivery)

Добавьте в таблицу `delivery`:

```python
[
    {"user_id": 1, "email": "alice@example.com", "address": "Wonderland 1, London", "phone": "+79997776655"},
    {"user_id": 2, "email": "bob@example.com", "address": "Builder St 123, London", "phone": "+44-20-7946-0002"},
    {"user_id": 3, "email": None, "address": None, "phone": None},
    {"user_id": 4, "email": "diana@example.com", "address": "Princess Palace, London", "phone": None},
    {"user_id": 5, "email": None, "address": "Smith Lane 78, Dublin", "phone": "+353-1-234-5678"},
]
```

**Требования:**
- Используйте `session.add_all()`.
- Выведите количество добавленных записей.

---

#### Ассоциация пользователей и книг

Добавьте в таблицу `user_book_association`:

```python
[
    {"user_id": 1, "book_id": 1},
    {"user_id": 2, "book_id": 2},
    {"user_id": 3, "book_id": 3},
    {"user_id": 4, "book_id": 1},
    {"user_id": 1, "book_id": 2},
    {"user_id": 3, "book_id": 1},
    {"user_id": 3, "book_id": 10},
]
```

**Требования:**
- Используйте `session.add_all()`.
- Выведите количество добавленных записей.

---

3.Запросы:
- Найдите топ-3 самые популярные книги. Используйте limit(3), чтобы ограничить
  выборку.

- Выведите информацию в из таблиц в следующем виде:
  <Полное имя пользователя> (<Имя пользователя>):
      Купленные книги:
          <Название книги> - <Автор> (<Жанр>); <Цена> руб.
      Итого: <Общая сумма, потраченная пользователем на книги> руб.

  Пример:
  Alice Wonderland (alice):
    Купленные книги:
        Мастер и Маргарита - Михаил Булгаков (Роман); 890.0 руб.
        Преступление и наказание - Федор Достоевский (Роман); 750.0 руб.
    Итого: 1640.00 руб.

- Выведите пользователей, у кого нет хотя бы одного из полей: email, address,
  phone.

- Увеличьте цену всех книг на 5%. Верните через returning() названия книг и их
  новую цену. Выведите в формате
  <Название книги>: <Старая цена> -> <Новая цена> (<Разница>) руб.

- Сформируйте отчёт по магазину в формате:
```
1. Книги:
   - "1984": 2 шт. x 682.5 руб. = 1365.00 руб.
   - "Анна Каренина": 0 шт. x 997.5 руб. = 0.00 руб. (нет в наличии)
   - "Война и мир. Том 1": 1 шт. x 1260.0 руб. = 1260.00 руб.
   - "Маленький принц": 7 шт. x 472.5 руб. = 3307.50 руб.
   - "Мастер и Маргарита": 5 шт. x 934.5 руб. = 4672.50 руб.
   - "Портрет Дориана Грея": 0 шт. x 546.0 руб. = 0.00 руб. (нет в наличии)
   - "Преступление и наказание": 3 шт. x 787.5 руб. = 2362.50 руб.
   - "Собачье сердце": 4 шт. x 619.5 руб. = 2478.00 руб.
   - "Три товарища": 2 шт. x 724.5 руб. = 1449.00 руб.
   - "Убить пересмешника": 0 шт. x 577.5 руб. = 0.00 руб. (нет в наличии)

2. Активные читатели:
   - alice: 2 книга(и) (Мастер и Маргарита, Преступление и наказание)
   - bob: 1 книга(и) (Преступление и наказание)
   - charlie: 3 книга(и) (Мастер и Маргарита, 1984, Портрет Дориана Грея)
   - diana: 1 книга(и) (Мастер и Маргарита)

3. Самый популярный автор:
   - Михаил Булгаков (3 книга(и), 3 читатель(ей))
```

- Удалите пользователей без адреса. После удаления выведите удалённых
  пользователей, таблицу delivery, а также таблицу user_book_association.

- Удалите книгу с isbn=978-5-17-135043-1. После удаления выведите
  пользователей, которых затронуло удаление книги и таблицу
  user_book_association.

В качестве проверки используйте файл с выводом результатов запросов
(result.txt).
Формат вывода результата запросов можно посмотреть в этом же файле.

(*) Для очищения таблиц при тестировании используйте следующий код:
Base.metadata.drop_all(engine)

Составьте свой файлик с ответом 'my_result.txt' и запишите в него свои
результаты с помощью функции save_results_to_file.
Сравните содержимое файликов с помощью вызова функции compare_results.

---

## Пример решения

```
"""

import os

from sqlalchemy import (
    ForeignKey,
    String,
    create_engine,
    desc,
    func,
    or_,
    update, distinct,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

AVAILABLE = 1
NOT_AVAILABLE = 0

results = []


class ResultHandler:
    @staticmethod
    def add_section(title):
        results.append('\n' + '=' * 10 + title + '=' * 10)

    @staticmethod
    def save_results_to_file(filename='my_result.txt'):
        with open(filename, 'w', encoding='utf-8') as f:
            for line in results:
                f.write(line + '\n')

    @staticmethod
    def compare_results(my_file='my_result.txt', expected_file='result.txt'):
        print('\n' + '=' * 60)
        print('🔍 СРАВНЕНИЕ РЕЗУЛЬТАТОВ С ЭТАЛОНОМ')
        print('=' * 60)

        if not os.path.exists(expected_file):
            print(f'⚠️  Эталонный файл {expected_file} не найден.')
            print('   Создайте его вручную или скопируйте от преподавателя.')
            print('   Пропускаю сравнение...')
            return False

        if not os.path.exists(my_file):
            print(f'❌ Файл с моими результатами {my_file} не найден!')
            return False

        with open(my_file, 'r', encoding='utf-8') as f:
            my_lines = [line.rstrip() for line in f.readlines()]

        with open(expected_file, 'r', encoding='utf-8') as f:
            expected_lines = [line.rstrip() for line in f.readlines()]

        assert len(my_lines) == len(expected_lines), (
            f'Разное количество строк: моих {len(my_lines)}, эталон '
            f'{len(expected_lines)}'
        )

        differences = []
        for i, (my_line, expected_line) in enumerate(
            zip(my_lines, expected_lines)  # noqa
        ):
            if my_line != expected_line:
                differences.append(
                    f'Строка {i + 1}:\n  '
                    f'Моя:     {my_line}\n  Эталон:  {expected_line}'
                )

        if differences:
            print('❌ НАЙДЕНЫ РАЗЛИЧИЯ:')
            for diff in differences:
                print(diff)

            assert False, f'Найдено {len(differences)} различий с эталоном'  # noqa
        else:
            print('✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!')
            return True


class Base(DeclarativeBase):
    pass


class Book(Base):
    pass

    def __repr__(self):
        return (
            f'Book(id={self.id}, '
            f"title='{self.title}', "
            f"author='{self.author}', "
            f"year='{self.year}', "
            f"isbn='{self.isbn}', "
            f"pages='{self.pages}', "
            f"genre='{self.genre}', "
            f"count='{self.count}', "
            f"price='{self.price}')"
        )


class User(Base):
    pass

    def __repr__(self):
        return (
            f'User(id={self.id}, '
            f"name='{self.name}', "
            f"fullname='{self.fullname}')"
        )


class UserBookAssociation(Base):
    pass

    def __repr__(self):
        return (
            f'UserBookAssociation(user_id={self.user_id}, '
            f'book_id={self.book_id})'
        )


class Delivery(Base):
    pass

    def __repr__(self):
        return (
            f'Delivery(id={self.id}, '
            f'user_id={self.user_id}, '
            f"email='{self.email}', "
            f"address='{self.address}', "
            f"phone='{self.phone}')"
        )

class BookStore:
    def __init__(self, db_url='sqlite:///bookstore.db', echo=True):
        self.engine = create_engine(db_url, echo=echo)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def insert_books(self):
        pass

        with self.Session() as session:
            pass

            ResultHandler.add_section('2.1. Добавление книг')
            results.append(f'Добавлено книг: {...}')

    def insert_users(self):
        pass

        with ...:
            pass

            ResultHandler.add_section('2.2. Добавление пользователей')
            results.append(f'Добавлено пользователей: {...}')

    def insert_delivery(self):
        pass

        with ...:
            pass

            ResultHandler.add_section('2.3. Добавление данных доставки')
            results.append(f'Добавлено данных доставки: {...}')

    def insert_user_book_association(self):
        pass

        with ...:
            pass

            ResultHandler.add_section(
                '2.4. Добавление данных ассоциации пользователя и книги'
            )
            results.append(f'Добавлено ассоциаций: {...}')

    def get_top_books(self):
        with ...:
            ResultHandler.add_section('3.1. Топ-3 самые популярные книги')        
            pass

    def get_user_purchases_report(self):
        with ...:
            ResultHandler.add_section(
                '3.2. Информация о покупках пользователей'
            )
            pass

    def get_users_with_missing_delivery_data(self):
        with self.Session() as session:
            ResultHandler.add_section(
                '3.3. Пользователи с отсутствующими данными доставки'
            )
            pass

    def increase_prices_by_percent(self):
        with ...:
            ResultHandler.add_section('3.4. Увеличение цены на 5%')
            pass

    def generate_store_report(self):
        with ...:
            ResultHandler.add_section('3.5. Отчет по магазину')

            # ========== 1. Книги ==========
            results.append('\n1. Книги:')
            pass

            # ========== 2. Активные читатели ==========
            results.append('\n2. Активные читатели:')
            pass

            # ========== 3. Самый популярный автор ==========
            results.append('\n3. Самый популярный автор:')
            pass

    def delete_users_without_address(self):
        with ...:
            ResultHandler.add_section('3.6. Удаление пользователей без адреса')
            pass
            
            results.append('Удалены пользователи: ')
            pass

            results.append('\nОставшиеся записи в таблице delivery:')
            pass

            results.append(
                '\nОставшиеся записи в таблице user_book_association:'
            )
            pass

    def delete_book_by_isbn(self, isbn='978-5-17-135043-1'):
        with ...:
            ResultHandler.add_section('3.7. Удаление книги по ISBN')
            pass

            results.append('\nПользователи, у которых была эта книга:')
            pass

            results.append(
                '\nОставшиеся записи в таблице user_book_association:'
            )
            pass

    def run_all(self):
        self.create_tables()

        self.insert_books()
        self.insert_users()
        self.insert_delivery()
        self.insert_user_book_association()

        self.get_top_books()
        self.get_user_purchases_report()
        self.get_users_with_missing_delivery_data()
        self.increase_prices_by_percent()
        self.generate_store_report()
        self.delete_users_without_address()
        self.delete_book_by_isbn()

        print(*results, sep='\n')

        ResultHandler.save_results_to_file()

        ResultHandler.compare_results()


def main():
    bookstore = BookStore()
    bookstore.run_all()


if __name__ == '__main__':
    main()
```

---

## Ожидаемый результат

```
==========2.1. Добавление книг==========
Добавлено книг: 10

==========2.2. Добавление пользователей==========
Добавлено пользователей: 5

==========2.3. Добавление данных доставки==========
Добавлено данных доставки: 5

==========2.4. Добавление данных ассоциации пользователя и книги==========
Добавлено ассоциаций: 7

==========3.1. Топ-3 самые популярные книги==========
Book(id=1, title='Мастер и Маргарита', author='Михаил Булгаков', year='1967', isbn='978-5-17-135043-1', pages='480', genre='Роман', count='5', price='890.0') 3
Book(id=2, title='Преступление и наказание', author='Федор Достоевский', year='1866', isbn='978-5-04-116633-9', pages='672', genre='Роман', count='3', price='750.0') 2
Book(id=10, title='Портрет Дориана Грея', author='Оскар Уайльд', year='1890', isbn='978-5-04-116635-3', pages='320', genre='Роман', count='0', price='520.0') 1

==========3.2. Информация о покупках пользователей==========

Alice Wonderland (alice):
    Купленные книги:
        Мастер и Маргарита - Михаил Булгаков (Роман); 890.0 руб.
        Преступление и наказание - Федор Достоевский (Роман); 750.0 руб.
    Итого: 1640.00 руб.

Bob Builder (bob):
    Купленные книги:
        Преступление и наказание - Федор Достоевский (Роман); 750.0 руб.
    Итого: 750.00 руб.

Charlie Brown (charlie):
    Купленные книги:
        Мастер и Маргарита - Михаил Булгаков (Роман); 890.0 руб.
        1984 - Джордж Оруэлл (Антиутопия); 650.0 руб.
        Портрет Дориана Грея - Оскар Уайльд (Роман); 520.0 руб.
    Итого: 2060.00 руб.

Diana Princess (diana):
    Купленные книги:
        Мастер и Маргарита - Михаил Булгаков (Роман); 890.0 руб.
    Итого: 890.00 руб.

==========3.3. Пользователи с отсутствующими данными доставки==========
User(id=3, name='charlie', fullname='Charlie Brown')
User(id=4, name='diana', fullname='Diana Princess')
User(id=5, name='eve', fullname='Eve Smith')

==========3.4. Увеличение цены на 5%==========
Мастер и Маргарита: 890.00 -> 934.50 (44.50) руб.
Преступление и наказание: 750.00 -> 787.50 (37.50) руб.
1984: 650.00 -> 682.50 (32.50) руб.
Убить пересмешника: 550.00 -> 577.50 (27.50) руб.
Война и мир. Том 1: 1200.00 -> 1260.00 (60.00) руб.
Анна Каренина: 950.00 -> 997.50 (47.50) руб.
Собачье сердце: 590.00 -> 619.50 (29.50) руб.
Маленький принц: 450.00 -> 472.50 (22.50) руб.
Три товарища: 690.00 -> 724.50 (34.50) руб.
Портрет Дориана Грея: 520.00 -> 546.00 (26.00) руб.

==========3.5. Отчет по магазину==========

1. Книги:
   - "1984": 2 шт. x 682.5 руб. = 1365.00 руб.
   - "Анна Каренина": 0 шт. x 997.5 руб. = 0.00 руб. (нет в наличии)
   - "Война и мир. Том 1": 1 шт. x 1260.0 руб. = 1260.00 руб.
   - "Маленький принц": 7 шт. x 472.5 руб. = 3307.50 руб.
   - "Мастер и Маргарита": 5 шт. x 934.5 руб. = 4672.50 руб.
   - "Портрет Дориана Грея": 0 шт. x 546.0 руб. = 0.00 руб. (нет в наличии)
   - "Преступление и наказание": 3 шт. x 787.5 руб. = 2362.50 руб.
   - "Собачье сердце": 4 шт. x 619.5 руб. = 2478.00 руб.
   - "Три товарища": 2 шт. x 724.5 руб. = 1449.00 руб.
   - "Убить пересмешника": 0 шт. x 577.5 руб. = 0.00 руб. (нет в наличии)

2. Активные читатели:
   - alice: 2 книга(и) (Мастер и Маргарита, Преступление и наказание)
   - bob: 1 книга(и) (Преступление и наказание)
   - charlie: 3 книга(и) (Мастер и Маргарита, 1984, Портрет Дориана Грея)
   - diana: 1 книга(и) (Мастер и Маргарита)

3. Самый популярный автор:
   - Михаил Булгаков - 3 читателя

==========3.6. Удаление пользователей без адреса==========
Удалены пользователи: 
ID: 3, Name: charlie

Оставшиеся записи в таблице delivery:
  Delivery(id=1, user_id=1, email='alice@example.com', address='Wonderland 1, London', phone='+79997776655')
  Delivery(id=2, user_id=2, email='bob@example.com', address='Builder St 123, London', phone='+44-20-7946-0002')
  Delivery(id=4, user_id=4, email='diana@example.com', address='Princess Palace, London', phone='None')
  Delivery(id=5, user_id=5, email='None', address='Smith Lane 78, Dublin', phone='+353-1-234-5678')

Оставшиеся записи в таблице user_book_association:
  UserBookAssociation(user_id=1, book_id=1)
  UserBookAssociation(user_id=2, book_id=2)
  UserBookAssociation(user_id=4, book_id=1)
  UserBookAssociation(user_id=1, book_id=2)

==========3.7. Удаление книги по ISBN==========

Пользователи, у которых была эта книга:
  - Alice Wonderland (alice)
  - Diana Princess (diana)

Оставшиеся записи в таблице user_book_association:
  UserBookAssociation(user_id=2 (bob), book_id=2 (Преступление и наказание))
  UserBookAssociation(user_id=1 (alice), book_id=2 (Преступление и наказание))
```