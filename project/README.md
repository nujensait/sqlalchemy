# Итоговый проект: Система управления онлайн-курсами

## Содержание

- [Описание проекта](#описание-проекта)
- [Предметная область](#предметная-область)
  - [📚 Таблицы базы данных](#-таблицы-базы-данных)
    - [1. students — Студенты онлайн-школы](#1-students--студенты-онлайн-школы)
    - [2. teachers — Преподаватели](#2-teachers--преподаватели)
    - [3. courses — Учебные курсы](#3-courses--учебные-курсы)
    - [4. enrollments — Записи студентов на курсы](#4-enrollments--записи-студентов-на-курсы)
- [Архитектура проекта](#архитектура-проекта)
- [Реализованные возможности](#реализованные-возможности)
  - [✅ Операции CRUD](#-операции-crud)
  - [✅ Типы запросов](#-типы-запросов)
  - [✅ Оптимизация](#-оптимизация)
  - [✅ Архитектурные паттерны](#-архитектурные-паттерны)
- [Запуск проекта](#запуск-проекта)
  - [Установка зависимостей](#установка-зависимостей)
  - [Запуск демонстрации](#запуск-демонстрации)
  - [Проверка кода](#проверка-кода)
- [Демонстрационные данные](#демонстрационные-данные)
- [Пример вывода](#пример-вывода)
- [Технические детали](#технические-детали)
- [Пример запуска](#пример-запуска)
- [Дополнительная информация](#дополнительная-информация)

---

## Описание проекта

Демонстрационная база данных для управления онлайн-школой, реализованная с использованием **SQLAlchemy ORM 2.0** и архитектурных паттернов **Repository** и **Unit of Work**.

Проект демонстрирует навыки проектирования реляционных баз данных, работу со связями между таблицами, каскадное удаление и оптимизацию запросов.

---

## Предметная область

**Система управления онлайн-курсами** включает следующие сущности:

### 📚 Таблицы базы данных

#### 1. **students** — Студенты онлайн-школы

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | INTEGER | Уникальный идентификатор студента (PRIMARY KEY) |
| `email` | STRING | Email (логин), уникальный |
| `full_name` | STRING | Полное имя студента |
| `enrolled_at` | DATETIME | Дата и время регистрации |
| `is_active` | BOOLEAN | Статус активности (1 — активен, 0 — заблокирован) |

**Связи:**
- `one-to-many` с `enrollments` (один студент → много записей на курсы)

---

#### 2. **teachers** — Преподаватели

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | INTEGER | Уникальный идентификатор преподавателя (PRIMARY KEY) |
| `full_name` | STRING | Полное имя преподавателя |
| `department` | STRING | Название кафедры (CS, Math, Physics и т.д.) |
| `hire_date` | DATE | Дата найма на работу |
| `phone` | STRING(15) | Номер телефона (уникальный) |

**Связи:**
- `one-to-many` с `courses` (один преподаватель → много курсов)

---

#### 3. **courses** — Учебные курсы

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | INTEGER | Уникальный идентификатор курса (PRIMARY KEY) |
| `title` | STRING | Название курса (уникальное) |
| `description` | TEXT | Подробное описание курса |
| `credits` | INTEGER | Количество кредитных часов (по умолчанию 3) |
| `max_seats` | INTEGER | Максимальное количество студентов (по умолчанию 30) |
| `price` | FLOAT | Стоимость курса в рублях |
| `teacher_id` | INTEGER | ID преподавателя (FOREIGN KEY → `teachers.id`) |

**Связи:**
- `many-to-one` с `teachers` (много курсов → один преподаватель)
- `one-to-many` с `enrollments` (один курс → много записей студентов)

**Каскадные действия:**
- При удалении преподавателя: `ON DELETE SET NULL` (курс остаётся, `teacher_id` = NULL)

---

#### 4. **enrollments** — Записи студентов на курсы

Промежуточная таблица для реализации связи `many-to-many` между студентами и курсами.

| Поле | Тип | Описание |
|------|-----|----------|
| `student_id` | INTEGER | ID студента (PRIMARY KEY, FOREIGN KEY → `students.id`) |
| `course_id` | INTEGER | ID курса (PRIMARY KEY, FOREIGN KEY → `courses.id`) |
| `enrolled_at` | DATETIME | Дата и время записи на курс |
| `grade` | FLOAT | Оценка за курс (0-100, NULL если не выставлена) |
| `is_completed` | BOOLEAN | Флаг завершения курса (1 — завершён, 0 — в процессе) |

**Составной первичный ключ:** (`student_id`, `course_id`)

**Связи:**
- `many-to-one` с `students` (много записей → один студент)
- `many-to-one` с `courses` (много записей → один курс)

**Каскадные действия:**
- При удалении студента: `ON DELETE CASCADE` (все его записи удаляются)
- При удалении курса: `ON DELETE CASCADE` (все записи студентов удаляются)

---

## Архитектура проекта

```
project/
├── models.py                    # Модели данных (Student, Teacher, Course, Enrollment)
├── repositories/                # Паттерн Repository
│   ├── __init__.py
│   ├── base_repository.py       # Базовый репозиторий с CRUD операциями
│   ├── student_repository.py    # Репозиторий студентов
│   ├── teacher_repository.py    # Репозиторий преподавателей
│   ├── course_repository.py     # Репозиторий курсов
│   └── enrollment_repository.py # Репозиторий записей на курсы
├── unit_of_work.py              # Паттерн Unit of Work (управление транзакциями)
├── service.py                   # Сервисный слой (бизнес-логика)
├── main.py                      # Демонстрация работы системы
└── courses.db                   # База данных SQLite (создаётся при запуске)
```

---

## Реализованные возможности

### ✅ Операции CRUD

- **INSERT**: Добавление студентов, преподавателей, курсов, записей на курсы
- **UPDATE**: Выставление оценок, обновление цен курсов, изменение статуса активности
- **DELETE**: Удаление с каскадным удалением связанных записей
- **SELECT**: Получение данных с различными фильтрами и сортировками

### ✅ Типы запросов

- **WHERE**: Фильтрация активных студентов, поиск по email
- **JOIN**: Получение студентов с курсами и преподавателями
- **GROUP BY**: Подсчёт количества студентов на курсах, средние оценки
- **ORDER BY**: Сортировка курсов по популярности и цене
- **EXISTS/ANY**: Поиск студентов с незавершёнными курсами

### ✅ Оптимизация

- Использование `joinedload()` и `selectinload()` для предзагрузки связанных данных
- Отсутствие N+1 запросов
- Агрегирующие запросы выполняются на стороне БД (`func.count()`, `func.avg()`)
- Индексы на внешних ключах

### ✅ Архитектурные паттерны

- **Repository Pattern**: Абстракция доступа к данным
- **Unit of Work**: Управление транзакциями и координация репозиториев
- **Service Layer**: Инкапсуляция бизнес-логики

---

## Запуск проекта

### Установка зависимостей

```bash
# Установить зависимости через uv
uv sync

# Или через make
make install
```

### Запуск демонстрации

```bash
# Через make (рекомендуется)
make prj

# Или напрямую через Python
python -m project.main
```

### Проверка кода

```bash
# Форматирование кода
make format

# Проверка линтером
make lint

# Автоисправление замечаний
make lint-fix
```

---

## Демонстрационные данные

При запуске проекта автоматически создаются:

- **2 преподавателя**: Dr. Alan Turing (CS), Prof. Ada Lovelace (Math)
- **3 курса**: Python Programming, SQL for Data Science, Calculus I
- **3 студента**: John Doe, Jane Smith, Bob Brown
- **5 записей на курсы** с оценками и статусами завершения

---

## Пример вывода

```
📁 База данных: /project/courses.db

============================================================
📊 1. ДОБАВЛЕНИЕ ДАННЫХ (INSERT)
============================================================

➕ Добавление преподавателей...
   ✅ Добавлено преподавателей: 2

➕ Добавление курсов...
   ✅ Добавлено курсов: 3

============================================================
📊 4. ЗАПРОСЫ С JOIN
============================================================

🔗 Преподаватели и их курсы:

   Dr. Alan Turing (CS):
      📚 Python Programming (4 кредита, 299.0 руб.)
      📚 SQL for Data Science (3 кредита, 249.0 руб.)

   Prof. Ada Lovelace (Math):
      📚 Calculus I (5 кредита, 349.0 руб.)

============================================================
✅ ВСЕ ЗАПРОСЫ ВЫПОЛНЕНЫ УСПЕШНО
============================================================

📋 База данных скопирована: project/courses.db
```

---

## Технические детали

### База данных

- **СУБД**: SQLite
- **Расположение**: 
  - Файл: `project/courses.db`

### Зависимости

- **SQLAlchemy** >= 2.0.0
- **Python** >= 3.14

### Соответствие требованиям

- ✅ Минимум 4 таблицы
- ✅ Связи: one-to-many, many-to-one, many-to-many
- ✅ Каскадное удаление настроено
- ✅ Все типы запросов реализованы
- ✅ Запросы оптимизированы
- ✅ Docstring и аннотации типов для всех классов и методов
- ✅ Проходит проверку `ruff` без ошибок
- ✅ Красивый форматированный вывод
- ✅ Структура таблиц отличается от учебных примеров

---

## Дополнительная информация

Требования к проекту: [REQUIREMENTS.md](REQUIREMENTS.md)  

---

## Пример запуска

```bash
make prj

Запуск итогового проекта...
uv run python -m project.main
📁 База данных: /tmp/courses.db

🔍 SQL: PRAGMA main.table_info("courses")
🔍 SQL: PRAGMA temp.table_info("courses")
🔍 SQL: PRAGMA main.table_info("enrollments")
🔍 SQL: PRAGMA temp.table_info("enrollments")
🔍 SQL: PRAGMA main.table_info("students")
🔍 SQL: PRAGMA temp.table_info("students")
🔍 SQL: PRAGMA main.table_info("teachers")
🔍 SQL: PRAGMA temp.table_info("teachers")

🔍 SQL: 
CREATE TABLE students (
        id INTEGER NOT NULL, 
        email VARCHAR NOT NULL, 
        full_name VARCHAR NOT NULL, 
        enrolled_at DATETIME NOT NULL, 
        is_active BOOLEAN NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (email)
)

🔍 SQL: 
CREATE TABLE teachers (
        id INTEGER NOT NULL, 
        full_name VARCHAR NOT NULL, 
        department VARCHAR NOT NULL, 
        hire_date DATE, 
        phone VARCHAR(15), 
        PRIMARY KEY (id), 
        UNIQUE (phone)
)

🔍 SQL: 
CREATE TABLE courses (
        id INTEGER NOT NULL, 
        title VARCHAR NOT NULL, 
        description TEXT, 
        credits INTEGER NOT NULL, 
        max_seats INTEGER NOT NULL, 
        price FLOAT NOT NULL, 
        teacher_id INTEGER, 
        PRIMARY KEY (id), 
        UNIQUE (title), 
        FOREIGN KEY(teacher_id) REFERENCES teachers (id) ON DELETE SET NULL
)

🔍 SQL: 
CREATE TABLE enrollments (
        student_id INTEGER NOT NULL, 
        course_id INTEGER NOT NULL, 
        enrolled_at DATETIME NOT NULL, 
        grade FLOAT, 
        is_completed BOOLEAN NOT NULL, 
        PRIMARY KEY (student_id, course_id), 
        FOREIGN KEY(student_id) REFERENCES students (id) ON DELETE CASCADE, 
        FOREIGN KEY(course_id) REFERENCES courses (id) ON DELETE CASCADE
)

============================================================
📊 1. ДОБАВЛЕНИЕ ДАННЫХ (INSERT)
============================================================

➕ Добавление преподавателей...

🔍 SQL: INSERT INTO teachers (full_name, department, hire_date, phone) VALUES (?, ?, ?, ?)
   Параметры: ('Dr. Alan Turing', 'CS', '2020-01-15', '+1-555-0101')

🔍 SQL: INSERT INTO teachers (full_name, department, hire_date, phone) VALUES (?, ?, ?, ?)
   Параметры: ('Prof. Ada Lovelace', 'Math', '2019-08-20', '+1-555-0102')
   ✅ Добавлено преподавателей: 2

➕ Добавление курсов...

🔍 SQL: SELECT teachers.id AS teachers_id, teachers.full_name AS teachers_full_name, teachers.department AS teachers_department, teachers.hire_date AS teachers_hire_date, teachers.phone AS teachers_phone 
FROM teachers 
WHERE teachers.id = ?
   Параметры: (1,)

🔍 SQL: INSERT INTO courses (title, description, credits, max_seats, price, teacher_id) VALUES (?, ?, ?, ?, ?, ?)
   Параметры: ('Python Programming', 'Basics of Python', 4, 25, 299.0, 1)

🔍 SQL: INSERT INTO courses (title, description, credits, max_seats, price, teacher_id) VALUES (?, ?, ?, ?, ?, ?)
   Параметры: ('SQL for Data Science', 'Advanced queries', 3, 30, 249.0, 1)

🔍 SQL: SELECT teachers.id AS teachers_id, teachers.full_name AS teachers_full_name, teachers.department AS teachers_department, teachers.hire_date AS teachers_hire_date, teachers.phone AS teachers_phone 
FROM teachers 
WHERE teachers.id = ?
   Параметры: (2,)

🔍 SQL: INSERT INTO courses (title, description, credits, max_seats, price, teacher_id) VALUES (?, ?, ?, ?, ?, ?)
   Параметры: ('Calculus I', 'Limits and derivatives', 5, 35, 349.0, 2)
   ✅ Добавлено курсов: 3

➕ Добавление студентов...

🔍 SQL: INSERT INTO students (email, full_name, enrolled_at, is_active) VALUES (?, ?, ?, ?)
   Параметры: ('john@example.com', 'John Doe', '2026-05-23 00:03:41.375855', 1)

🔍 SQL: INSERT INTO students (email, full_name, enrolled_at, is_active) VALUES (?, ?, ?, ?)
   Параметры: ('jane@example.com', 'Jane Smith', '2026-05-23 00:03:41.376511', 1)

🔍 SQL: INSERT INTO students (email, full_name, enrolled_at, is_active) VALUES (?, ?, ?, ?)
   Параметры: ('bob@example.com', 'Bob Brown', '2026-05-23 00:03:41.376905', 0)
   ✅ Добавлено студентов: 3

➕ Запись студентов на курсы...

🔍 SQL: SELECT students.id AS students_id, students.email AS students_email, students.full_name AS students_full_name, students.enrolled_at AS students_enrolled_at, students.is_active AS students_is_active 
FROM students 
WHERE students.id = ?
   Параметры: (1,)

🔍 SQL: SELECT courses.id AS courses_id, courses.title AS courses_title, courses.description AS courses_description, courses.credits AS courses_credits, courses.max_seats AS courses_max_seats, courses.price AS courses_price, courses.teacher_id AS courses_teacher_id 
FROM courses 
WHERE courses.id = ?
   Параметры: (1,)

🔍 SQL: INSERT INTO enrollments (student_id, course_id, enrolled_at, grade, is_completed) VALUES (?, ?, ?, ?, ?)
   Параметры: (1, 1, '2026-05-23 00:03:41.404675', None, 0)

🔍 SQL: SELECT courses.id AS courses_id, courses.title AS courses_title, courses.description AS courses_description, courses.credits AS courses_credits, courses.max_seats AS courses_max_seats, courses.price AS courses_price, courses.teacher_id AS courses_teacher_id 
FROM courses 
WHERE courses.id = ?
   Параметры: (2,)

🔍 SQL: INSERT INTO enrollments (student_id, course_id, enrolled_at, grade, is_completed) VALUES (?, ?, ?, ?, ?)
   Параметры: (1, 2, '2026-05-23 00:03:41.405619', None, 0)

🔍 SQL: SELECT students.id AS students_id, students.email AS students_email, students.full_name AS students_full_name, students.enrolled_at AS students_enrolled_at, students.is_active AS students_is_active 
FROM students 
WHERE students.id = ?
   Параметры: (2,)

🔍 SQL: INSERT INTO enrollments (student_id, course_id, enrolled_at, grade, is_completed) VALUES (?, ?, ?, ?, ?)
   Параметры: (2, 1, '2026-05-23 00:03:41.406228', None, 0)

🔍 SQL: SELECT courses.id AS courses_id, courses.title AS courses_title, courses.description AS courses_description, courses.credits AS courses_credits, courses.max_seats AS courses_max_seats, courses.price AS courses_price, courses.teacher_id AS courses_teacher_id 
FROM courses 
WHERE courses.id = ?
   Параметры: (3,)

🔍 SQL: INSERT INTO enrollments (student_id, course_id, enrolled_at, grade, is_completed) VALUES (?, ?, ?, ?, ?)
   Параметры: (2, 3, '2026-05-23 00:03:41.406779', None, 0)

🔍 SQL: SELECT students.id AS students_id, students.email AS students_email, students.full_name AS students_full_name, students.enrolled_at AS students_enrolled_at, students.is_active AS students_is_active 
FROM students 
WHERE students.id = ?
   Параметры: (3,)

🔍 SQL: INSERT INTO enrollments (student_id, course_id, enrolled_at, grade, is_completed) VALUES (?, ?, ?, ?, ?)
   Параметры: (3, 2, '2026-05-23 00:03:41.407276', None, 0)
   ✅ Создано записей: 5

============================================================
📊 2. ОБНОВЛЕНИЕ ДАННЫХ (UPDATE)
============================================================

🔄 Выставление оценок студентам...

🔍 SQL: SELECT students.id AS students_id, students.email AS students_email, students.full_name AS students_full_name, students.enrolled_at AS students_enrolled_at, students.is_active AS students_is_active 
FROM students 
WHERE students.id = ?
   Параметры: (1,)

🔍 SQL: SELECT courses.id AS courses_id, courses.title AS courses_title, courses.description AS courses_description, courses.credits AS courses_credits, courses.max_seats AS courses_max_seats, courses.price AS courses_price, courses.teacher_id AS courses_teacher_id 
FROM courses 
WHERE courses.id = ?
   Параметры: (1,)

🔍 SQL: SELECT enrollments.student_id AS enrollments_student_id, enrollments.course_id AS enrollments_course_id, enrollments.enrolled_at AS enrollments_enrolled_at, enrollments.grade AS enrollments_grade, enrollments.is_completed AS enrollments_is_completed 
FROM enrollments 
WHERE enrollments.student_id = ? AND enrollments.course_id = ?
   Параметры: (1, 1)

🔍 SQL: UPDATE enrollments SET grade=? WHERE enrollments.student_id = ? AND enrollments.course_id = ?
   Параметры: (85.5, 1, 1)

🔍 SQL: SELECT enrollments.student_id AS enrollments_student_id, enrollments.course_id AS enrollments_course_id, enrollments.enrolled_at AS enrollments_enrolled_at, enrollments.grade AS enrollments_grade, enrollments.is_completed AS enrollments_is_completed 
FROM enrollments 
WHERE enrollments.student_id = ? AND enrollments.course_id = ?
   Параметры: (1, 1)

🔍 SQL: UPDATE enrollments SET is_completed=? WHERE enrollments.student_id = ? AND enrollments.course_id = ?
   Параметры: (1, 1, 1)

🔍 SQL: SELECT students.id AS students_id, students.email AS students_email, students.full_name AS students_full_name, students.enrolled_at AS students_enrolled_at, students.is_active AS students_is_active 
FROM students 
WHERE students.id = ?
   Параметры: (2,)

🔍 SQL: SELECT enrollments.student_id AS enrollments_student_id, enrollments.course_id AS enrollments_course_id, enrollments.enrolled_at AS enrollments_enrolled_at, enrollments.grade AS enrollments_grade, enrollments.is_completed AS enrollments_is_completed 
FROM enrollments 
WHERE enrollments.student_id = ? AND enrollments.course_id = ?
   Параметры: (2, 1)

🔍 SQL: UPDATE enrollments SET grade=? WHERE enrollments.student_id = ? AND enrollments.course_id = ?
   Параметры: (92.0, 2, 1)

🔍 SQL: SELECT enrollments.student_id AS enrollments_student_id, enrollments.course_id AS enrollments_course_id, enrollments.enrolled_at AS enrollments_enrolled_at, enrollments.grade AS enrollments_grade, enrollments.is_completed AS enrollments_is_completed 
FROM enrollments 
WHERE enrollments.student_id = ? AND enrollments.course_id = ?
   Параметры: (2, 1)

🔍 SQL: UPDATE enrollments SET is_completed=? WHERE enrollments.student_id = ? AND enrollments.course_id = ?
   Параметры: (1, 2, 1)

🔍 SQL: SELECT courses.id AS courses_id, courses.title AS courses_title, courses.description AS courses_description, courses.credits AS courses_credits, courses.max_seats AS courses_max_seats, courses.price AS courses_price, courses.teacher_id AS courses_teacher_id 
FROM courses 
WHERE courses.id = ?
   Параметры: (3,)

🔍 SQL: SELECT enrollments.student_id AS enrollments_student_id, enrollments.course_id AS enrollments_course_id, enrollments.enrolled_at AS enrollments_enrolled_at, enrollments.grade AS enrollments_grade, enrollments.is_completed AS enrollments_is_completed 
FROM enrollments 
WHERE enrollments.student_id = ? AND enrollments.course_id = ?
   Параметры: (2, 3)

🔍 SQL: UPDATE enrollments SET grade=? WHERE enrollments.student_id = ? AND enrollments.course_id = ?
   Параметры: (78.0, 2, 3)

🔍 SQL: SELECT enrollments.student_id AS enrollments_student_id, enrollments.course_id AS enrollments_course_id, enrollments.enrolled_at AS enrollments_enrolled_at, enrollments.grade AS enrollments_grade, enrollments.is_completed AS enrollments_is_completed 
FROM enrollments 
WHERE enrollments.student_id = ? AND enrollments.course_id = ?
   Параметры: (2, 3)

🔍 SQL: UPDATE enrollments SET is_completed=? WHERE enrollments.student_id = ? AND enrollments.course_id = ?
   Параметры: (1, 2, 3)
   ✅ Оценки выставлены

🔄 Обновление цены курса...

🔍 SQL: SELECT courses.id AS courses_id, courses.title AS courses_title, courses.description AS courses_description, courses.credits AS courses_credits, courses.max_seats AS courses_max_seats, courses.price AS courses_price, courses.teacher_id AS courses_teacher_id 
FROM courses 
WHERE courses.id = ?
   Параметры: (1,)

🔍 SQL: UPDATE courses SET price=? WHERE courses.id = ?
   Параметры: (349.0, 1)

🔍 SQL: SELECT courses.id AS courses_id, courses.title AS courses_title, courses.description AS courses_description, courses.credits AS courses_credits, courses.max_seats AS courses_max_seats, courses.price AS courses_price, courses.teacher_id AS courses_teacher_id 
FROM courses 
WHERE courses.id = ?
   Параметры: (1,)
   ✅ Цена "Python Programming" изменена: 299.0 → 349.0 руб.

============================================================
📊 3. ЗАПРОСЫ С WHERE
============================================================

🔍 Активные студенты:

🔍 SQL: SELECT students.id, students.email, students.full_name, students.enrolled_at, students.is_active 
FROM students 
WHERE students.is_active = 1
   - John Doe (john@example.com)
   - Jane Smith (jane@example.com)

============================================================
📊 4. ЗАПРОСЫ С JOIN
============================================================

🔗 Преподаватели и их курсы:

🔍 SQL: SELECT teachers.id, teachers.full_name, teachers.department, teachers.hire_date, teachers.phone, courses_1.id AS id_1, courses_1.title, courses_1.description, courses_1.credits, courses_1.max_seats, courses_1.price, courses_1.teacher_id 
FROM teachers LEFT OUTER JOIN courses AS courses_1 ON teachers.id = courses_1.teacher_id

   Dr. Alan Turing (CS):
      📚 Python Programming (4 кредита, 349.0 руб.)
      📚 SQL for Data Science (3 кредита, 249.0 руб.)

   Prof. Ada Lovelace (Math):
      📚 Calculus I (5 кредита, 349.0 руб.)

============================================================
📊 5. ЗАПРОСЫ С GROUP BY
============================================================

📊 Количество студентов на каждом курсе:

🔍 SQL: SELECT courses.id, courses.title, courses.description, courses.credits, courses.max_seats, courses.price, courses.teacher_id, count(enrollments.student_id) AS cnt 
FROM courses JOIN enrollments ON courses.id = enrollments.course_id GROUP BY courses.id ORDER BY count(enrollments.student_id) DESC
   SQL for Data Science: 2 студента(ов)
   Python Programming: 2 студента(ов)
   Calculus I: 1 студента(ов)

📊 Средняя оценка по курсам:

🔍 SQL: SELECT courses.id, courses.title, courses.description, courses.credits, courses.max_seats, courses.price, courses.teacher_id, avg(enrollments.grade) AS avg_grade 
FROM courses JOIN enrollments ON courses.id = enrollments.course_id 
WHERE enrollments.grade IS NOT NULL GROUP BY courses.id ORDER BY avg(enrollments.grade) DESC
   Python Programming: 88.75
   Calculus I: 78.00

============================================================
📊 6. ЗАПРОСЫ С ORDER BY
============================================================

📈 Топ-3 самых популярных курса:

🔍 SQL: SELECT courses.id, courses.title, courses.description, courses.credits, courses.max_seats, courses.price, courses.teacher_id, count(enrollments.student_id) AS cnt 
FROM courses JOIN enrollments ON courses.id = enrollments.course_id GROUP BY courses.id ORDER BY count(enrollments.student_id) DESC
 LIMIT ? OFFSET ?
   Параметры: (3, 0)
   1. SQL for Data Science — 2 студента(ов)
   2. Python Programming — 2 студента(ов)
   3. Calculus I — 1 студента(ов)

💰 Курсы, отсортированные по цене (убывание):

🔍 SQL: SELECT courses.id, courses.title, courses.description, courses.credits, courses.max_seats, courses.price, courses.teacher_id 
FROM courses ORDER BY courses.price DESC
   Python Programming: 349.0 руб.
   Calculus I: 349.0 руб.
   SQL for Data Science: 249.0 руб.

============================================================
📊 7. ЗАПРОСЫ С EXISTS/ANY
============================================================

🔍 Студенты с незавершёнными курсами:

🔍 SQL: SELECT enrollments.student_id, enrollments.course_id, enrollments.enrolled_at, enrollments.grade, enrollments.is_completed, students_1.id, students_1.email, students_1.full_name, students_1.enrolled_at AS enrolled_at_1, students_1.is_active, courses_1.id AS id_1, courses_1.title, courses_1.description, courses_1.credits, courses_1.max_seats, courses_1.price, courses_1.teacher_id 
FROM enrollments LEFT OUTER JOIN students AS students_1 ON students_1.id = enrollments.student_id LEFT OUTER JOIN courses AS courses_1 ON courses_1.id = enrollments.course_id 
WHERE enrollments.is_completed = 0
   - John Doe: SQL for Data Science (оценка не выставлена)
   - Bob Brown: SQL for Data Science (оценка не выставлена)

============================================================
📊 8. УДАЛЕНИЕ ДАННЫХ (DELETE)
============================================================

🗑️  Удаление студента (каскадное удаление записей)...

🔍 SQL: SELECT enrollments.student_id, enrollments.course_id, enrollments.enrolled_at, enrollments.grade, enrollments.is_completed 
FROM enrollments

🔍 SQL: SELECT enrollments.student_id AS enrollments_student_id, enrollments.course_id AS enrollments_course_id, enrollments.enrolled_at AS enrollments_enrolled_at, enrollments.grade AS enrollments_grade, enrollments.is_completed AS enrollments_is_completed 
FROM enrollments 
WHERE ? = enrollments.student_id
   Параметры: (3,)

🔍 SQL: DELETE FROM enrollments WHERE enrollments.student_id = ? AND enrollments.course_id = ?
   Параметры: (3, 2)

🔍 SQL: DELETE FROM students WHERE students.id = ?
   Параметры: (3,)

🔍 SQL: SELECT enrollments.student_id, enrollments.course_id, enrollments.enrolled_at, enrollments.grade, enrollments.is_completed 
FROM enrollments
   ✅ Удалён студент: Bob Brown
   ✅ Записей до удаления: 5, после: 4

🗑️  Удаление преподавателя (в курсах teacher_id = NULL)...

🔍 SQL: SELECT teachers.id AS teachers_id, teachers.full_name AS teachers_full_name, teachers.department AS teachers_department, teachers.hire_date AS teachers_hire_date, teachers.phone AS teachers_phone 
FROM teachers 
WHERE teachers.id = ?
   Параметры: (2,)

🔍 SQL: SELECT courses.id AS courses_id, courses.title AS courses_title, courses.description AS courses_description, courses.credits AS courses_credits, courses.max_seats AS courses_max_seats, courses.price AS courses_price, courses.teacher_id AS courses_teacher_id 
FROM courses 
WHERE ? = courses.teacher_id
   Параметры: (2,)

🔍 SQL: UPDATE courses SET teacher_id=? WHERE courses.id = ?
   Параметры: (None, 3)

🔍 SQL: DELETE FROM teachers WHERE teachers.id = ?
   Параметры: (2,)
   ✅ Удалён преподаватель: Prof. Ada Lovelace

🔍 SQL: SELECT courses.id AS courses_id, courses.title AS courses_title, courses.description AS courses_description, courses.credits AS courses_credits, courses.max_seats AS courses_max_seats, courses.price AS courses_price, courses.teacher_id AS courses_teacher_id 
FROM courses 
WHERE courses.id = ?
   Параметры: (3,)
   ✅ Курс "Calculus I" остался, teacher_id = None

============================================================
✅ ВСЕ ЗАПРОСЫ ВЫПОЛНЕНЫ УСПЕШНО
============================================================

📋 База данных скопирована: project/courses.db
```
