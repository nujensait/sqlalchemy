# Содержание

- [Инструкция по выполнению домашнего задания](#инструкция-по-выполнению-домашнего-задания)
- [Распределение процентов](#распределение-процентов)
- [Общие критерии](#общие-критерии)
- [Условие задачи](#условие-задачи)
- [Ожидаемый результат](#ожидаемый-результат)

## Инструкция

1. 📥 Переключитесь в PyCharm на ветку `main` и обновите её с помощью `Update Project`...

🌿 Создайте новую ветку под названием `hw4`.

💻 Напишите код, необходимый для решения задачи (условие задачи находится во вложении к домашнему заданию).

✨ Выполните автоформатирование кода:
```
uv run ruff format
uv run ruff check --fix
```

📍Если есть ошибки - исправьте.

🔀 Выполните PR в ветку `main` и добавьте преподавателя в `Reviewers`.

---

📌 В качестве ответа приложите ссылку на PR.

ℹ️ Пример ссылки: `https://github.com/Username/SQLAlchemyCourse/pull/1`

---

## Распределение процентов

➡️ **100 %** — Все задачи выполнены в полном объёме и без замечаний

➡️ **90 - 99 %** — Выполнены все задачи, но есть мелкие недочеты, которые не влияют на результат. Нет ошибок PEP8.

➡️ **80 - 89 %** — Выполнены все задачи, но есть недочеты, которые не влияют на результат. Нет ошибок PEP8.

➡️ **75 - 79 %** — Выполнены все задачи, но есть недочеты, которые частично влияют на результат (максимум 1 некорректный результат). Есть ошибки PEP8 (не более 5 ошибок).

➡️ **Менее 75 %** — Задание не выполнено или выполнено с критическими ошибками.

---

## Общие критерии

**⚙️ Функциональность.**
- Прохождение тестов или проверка с верным ответом.
- Соответствие заданию.
- Отсутствие ошибок исполнения: код не падает с `SyntaxError`, `NameError`, `TypeError` или `AttributeError` при стандартных входных данных.

**📖 PEP8 (читаемость и стиль).**
- Замечания, связанные со стандартом PEP8 (например, избыточное количество пробелов, отступов или символов в строке, некорректные названия переменных).
- Проверяется при помощи `uv run ruff check`.

**🧠 Логика и структура.**
- Соблюдение принципов разработки кода:
  - **YAGNI** (You Aren’t Gonna Need It): не пишите код, если думаете, что он пригодится позже.
  - **DRY** (Don’t Repeat Yourself): не дублируйте код.
  - **KISS** (Keep It Simple, Stupid): не придумывайте к задаче более сложного решения, чем ей требуется.

**🛡️ Безопасность и надёжность.**
- Предварительная проверка.
- Обработка исключений.
- Закрытие ресурсов.

**📚 Документация, аннотации и комментарии.**
- Docstring для каждой функции и класса.
- Использование аннотаций в функциях, методах и переменных.
- Отсутствие закомментированного кода.
- Комментарии объясняют **ПОЧЕМУ** код написан так, а не **ЧТО** он делает (что должно быть очевидно из кода).

---

## Условие задачи

> Библиотека с книгами и пользователями
>
> **❗Данную домашнюю работу выполнять, используя SQLAlchemy ORM и Session!**

### 1. Создайте базу данных `bookstore.db`

`Book` и `User` — названия классов.

#### Таблица `Book`

| Поле      | Тип      | Ограничения                   | Описание                        |
|-----------|----------|-------------------------------|---------------------------------|
| id        | INTEGER  | PRIMARY KEY AUTOINCREMENT     | Уникальный идентификатор        |
| title     | STRING   | NOT NULL                      | Название книги                  |
| author    | STRING   | NOT NULL                      | Автор книги                     |
| year      | INTEGER  |                               | Год издания                     |
| isbn      | STRING   | UNIQUE                        | ISBN книги                      |
| pages     | INTEGER  | DEFAULT 0                     | Количество страниц              |
| genre     | STRING   |                               | Жанр                            |
| available | INTEGER  | DEFAULT 1                     | Доступна ли книга (1 — да, 0 — нет) |

Проверьте, что таблица создалась.

#### Таблица `User`

| Поле     | Тип          | Ограничения                   | Описание                    |
|----------|--------------|-------------------------------|-----------------------------|
| id       | INTEGER      | PRIMARY KEY AUTOINCREMENT     | Уникальный идентификатор    |
| name     | STRING(30)   | NOT NULL, UNIQUE              | Ник пользователя            |
| fullname | STRING(50)   |                               | ФИО пользователя            |
| book_id  | INTEGER      | FOREIGN KEY, NOT NULL         | ID взятой книги             |

Проверьте, что таблица создалась.

### 2. Заполнение таблиц данными

#### Добавление книг

Добавьте в таблицу `books` следующие книги:

```python
[
    {
        'title': 'Мастер и Маргарита',
        'author': 'Михаил Булгаков',
        'year': 1967,
        'isbn': '978-5-17-135043-1',
        'pages': 480,
        'genre': 'Роман',
        'available': 1,
    },
    {
        'title': 'Преступление и наказание',
        'author': 'Федор Достоевский',
        'year': 1866,
        'isbn': '978-5-04-116633-9',
        'pages': 672,
        'genre': 'Роман',
        'available': 1,
    },
    {
        'title': '1984',
        'author': 'Джордж Оруэлл',
        'year': 1949,
        'isbn': '978-5-17-137262-4',
        'pages': 320,
        'genre': 'Антиутопия',
        'available': 1,
    },
    {
        'title': 'Убить пересмешника',
        'author': 'Харпер Ли',
        'year': 1960,
        'isbn': '978-5-04-116631-5',
        'pages': 416,
        'genre': 'Роман',
        'available': 0,
    },
    {
        'title': 'Война и мир. Том 1',
        'author': 'Лев Толстой',
        'year': 1867,
        'isbn': '978-5-17-135042-4',
        'pages': 720,
        'genre': 'Роман-эпопея',
        'available': 1,
    },
    {
        'title': 'Анна Каренина',
        'author': 'Лев Толстой',
        'year': 1877,
        'isbn': '978-5-04-116632-2',
        'pages': 864,
        'genre': 'Роман',
        'available': 0,
    },
    {
        'title': 'Собачье сердце',
        'author': 'Михаил Булгаков',
        'year': 1925,
        'isbn': '978-5-17-135044-8',
        'pages': 352,
        'genre': 'Повесть',
        'available': 1,
    },
    {
        'title': 'Маленький принц',
        'author': 'Антуан де Сент-Экзюпери',
        'year': 1943,
        'isbn': '978-5-04-116634-6',
        'pages': 96,
        'genre': 'Сказка',
        'available': 1,
    },
    {
        'title': 'Три товарища',
        'author': 'Эрих Мария Ремарк',
        'year': 1936,
        'isbn': '978-5-17-137263-1',
        'pages': 384,
        'genre': 'Роман',
        'available': 1,
    },
    {
        'title': 'Портрет Дориана Грея',
        'author': 'Оскар Уайльд',
        'year': 1890,
        'isbn': '978-5-04-116635-3',
        'pages': 320,
        'genre': 'Роман',
        'available': 0,
    },
]
```

**Требования:**
- Используйте `session.add_all(list_books)` для добавления данных в сеанс, где `list_books` — список объектов `Book`.
- Получите `id` добавляемых книг с помощью метода `flush()`.
- Выведите количество добавленных книг как длину полученного списка `id` книг.

**Подсказки:**
- Для генерации списка объектов из словаря можно использовать конструкцию:  
  `books = [Book(**data) for data in books_data]`, где `books_data` — список словарей.

#### Добавление пользователей

Добавьте в таблицу `users` следующие данные:

```python
[
    {'name': 'alice', 'fullname': 'Alice Wonderland', 'book_id': 1},
    {'name': 'bob', 'fullname': 'Bob Builder', 'book_id': 3},
    {'name': 'charlie', 'fullname': 'Charlie Brown', 'book_id': 2},
    {'name': 'diana', 'fullname': 'Diana Princess', 'book_id': 7},
    {'name': 'eve', 'fullname': 'Eve Smith', 'book_id': 5},
]
```

**Требования:**
- Используйте `session.add_all()`.
- `id` книг соответствуют номерам элементов из списка книг.
- Выведите количество добавленных пользователей через длину списка объектов `User`.

### 3. SELECT-запросы

Напишите следующие запросы для получения данных:

- Все книги (все поля)
- Все пользователи (все поля)
- Доступные книги (`available = 1`)
- Книги, авторы (`author`) которых имеют букву "э" в названии
- Доступные книги, год которых меньше 1900
- Ник пользователя (`name`) и ФИО пользователя (`fullname`)
- Ник пользователя, ФИО пользователя, название книги (`title`) (join можно использовать так же, как и раньше)

В качестве проверки используйте файл с выводом результатов запросов (`result.txt`).  
Формат вывода результата запросов можно посмотреть в этом же файле.

> \*Для очищения таблиц при тестировании используйте следующий код:  
> `Base.metadata.drop_all(engine)`

Составьте свой файлик с ответом `my_result.txt` и запишите в него свои результаты с помощью функции `save_results_to_file`.  
Сравните содержимое файликов с помощью вызова функции `compare_results`.

```
"""

import os

from sqlalchemy.orm import DeclarativeBase, sessionmaker

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


class User(Base):
    pass


class LibraryORM:
    def __init__(self, db_url='sqlite:///bookstore.db', echo=True):
        self.engine = ...  # TODO: создание движка
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        # TODO: здесь должно быть удаление таблиц и их создание через metadata
        pass

    def insert_books(self):
        pass

        with ...:
            pass

            ResultHandler.add_section('2.1. Добавление книг')
            results.append(f'Добавлено книг: {...}')

    def insert_users(self):
        pass

        with ...:
            pass

            ResultHandler.add_section('2.2. Добавление пользователей')
            results.append(f'Добавлено пользователей: {...}')

    def execute_queries(self):
        with ...:
            ResultHandler.add_section('3.1. Все книги (все поля)')
            pass

            ResultHandler.add_section('3.2. Все пользователи (все поля)')
            pass

            ResultHandler.add_section('3.3. Доступные книги (available = 1)')
            pass

            ResultHandler.add_section(
                "3.4. Книги, авторы которых имеют букву 'э'"
            )
            pass

            ResultHandler.add_section(
                '3.5. Доступные книги, год которых меньше 1900'
            )
            pass

            ResultHandler.add_section('3.6. Ник и ФИО пользователей')
            pass

            ResultHandler.add_section('3.7. Пользователи и их книги')
            pass

    def run_all(self):
        self.create_tables()

        self.insert_books()
        self.insert_users()

        self.execute_queries()

        print(*results, sep='\n')

        ResultHandler.save_results_to_file()

        ResultHandler.compare_results()


def main():
    library = LibraryORM()
    library.run_all()


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

==========3.1. Все книги (все поля)==========
Book(id=1, title='Мастер и Маргарита', author='Михаил Булгаков', year=1967, isbn='978-5-17-135043-1', pages=480, genre='Роман', available=1)
Book(id=2, title='Преступление и наказание', author='Федор Достоевский', year=1866, isbn='978-5-04-116633-9', pages=672, genre='Роман', available=1)
Book(id=3, title='1984', author='Джордж Оруэлл', year=1949, isbn='978-5-17-137262-4', pages=320, genre='Антиутопия', available=1)
Book(id=4, title='Убить пересмешника', author='Харпер Ли', year=1960, isbn='978-5-04-116631-5', pages=416, genre='Роман', available=0)
Book(id=5, title='Война и мир. Том 1', author='Лев Толстой', year=1867, isbn='978-5-17-135042-4', pages=720, genre='Роман-эпопея', available=1)
Book(id=6, title='Анна Каренина', author='Лев Толстой', year=1877, isbn='978-5-04-116632-2', pages=864, genre='Роман', available=0)
Book(id=7, title='Собачье сердце', author='Михаил Булгаков', year=1925, isbn='978-5-17-135044-8', pages=352, genre='Повесть', available=1)
Book(id=8, title='Маленький принц', author='Антуан де Сент-Экзюпери', year=1943, isbn='978-5-04-116634-6', pages=96, genre='Сказка', available=1)
Book(id=9, title='Три товарища', author='Эрих Мария Ремарк', year=1936, isbn='978-5-17-137263-1', pages=384, genre='Роман', available=1)
Book(id=10, title='Портрет Дориана Грея', author='Оскар Уайльд', year=1890, isbn='978-5-04-116635-3', pages=320, genre='Роман', available=0)

==========3.2. Все пользователи (все поля)==========
User(id=1, name='alice', fullname='Alice Wonderland', book_id=1)
User(id=2, name='bob', fullname='Bob Builder', book_id=3)
User(id=3, name='charlie', fullname='Charlie Brown', book_id=2)
User(id=4, name='diana', fullname='Diana Princess', book_id=7)
User(id=5, name='eve', fullname='Eve Smith', book_id=5)

==========3.3. Доступные книги (available = 1)==========
Book(id=1, title='Мастер и Маргарита', author='Михаил Булгаков', year=1967, isbn='978-5-17-135043-1', pages=480, genre='Роман', available=1)
Book(id=2, title='Преступление и наказание', author='Федор Достоевский', year=1866, isbn='978-5-04-116633-9', pages=672, genre='Роман', available=1)
Book(id=3, title='1984', author='Джордж Оруэлл', year=1949, isbn='978-5-17-137262-4', pages=320, genre='Антиутопия', available=1)
Book(id=5, title='Война и мир. Том 1', author='Лев Толстой', year=1867, isbn='978-5-17-135042-4', pages=720, genre='Роман-эпопея', available=1)
Book(id=7, title='Собачье сердце', author='Михаил Булгаков', year=1925, isbn='978-5-17-135044-8', pages=352, genre='Повесть', available=1)
Book(id=8, title='Маленький принц', author='Антуан де Сент-Экзюпери', year=1943, isbn='978-5-04-116634-6', pages=96, genre='Сказка', available=1)
Book(id=9, title='Три товарища', author='Эрих Мария Ремарк', year=1936, isbn='978-5-17-137263-1', pages=384, genre='Роман', available=1)

==========3.4. Книги, авторы которых имеют букву 'э'==========
Book(id=3, title='1984', author='Джордж Оруэлл', year=1949, isbn='978-5-17-137262-4', pages=320, genre='Антиутопия', available=1)

==========3.5. Доступные книги, год которых меньше 1900==========
Book(id=2, title='Преступление и наказание', author='Федор Достоевский', year=1866, isbn='978-5-04-116633-9', pages=672, genre='Роман', available=1)
Book(id=5, title='Война и мир. Том 1', author='Лев Толстой', year=1867, isbn='978-5-17-135042-4', pages=720, genre='Роман-эпопея', available=1)

==========3.6. Ник и ФИО пользователей==========
alice: Alice Wonderland
bob: Bob Builder
charlie: Charlie Brown
diana: Diana Princess
eve: Eve Smith

==========3.7. Пользователи и их книги==========
alice (Alice Wonderland): Мастер и Маргарита
bob (Bob Builder): 1984
charlie (Charlie Brown): Преступление и наказание
diana (Diana Princess): Собачье сердце
eve (Eve Smith): Война и мир. Том 1
```