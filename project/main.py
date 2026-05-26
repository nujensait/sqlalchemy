"""Главный файл для демонстрации работы системы управления курсами."""

import os
import shutil
from datetime import date
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from project.infrastructure.database import Base
from project.infrastructure.unit_of_work import UnitOfWork
from project.service import CourseManagementService


@event.listens_for(Engine, 'before_cursor_execute')
def receive_before_cursor_execute(
    conn, cursor, statement, parameters, context, executemany
):  # type: ignore
    """Выводит SQL запросы перед выполнением.

    Args:
        conn: Соединение
        cursor: Курсор
        statement: SQL запрос
        parameters: Параметры запроса
        context: Контекст
        executemany: Флаг множественного выполнения
    """
    print(f'\n🔍 SQL: {statement}')
    if parameters:
        print(f'   Параметры: {parameters}')


def print_section(title: str) -> None:
    """Выводит заголовок раздела.

    Args:
        title: Название раздела
    """
    print('\n' + '=' * 60)
    print(f'📊 {title}')
    print('=' * 60)


def main() -> None:
    """Основная функция для демонстрации работы системы."""
    if os.name == 'posix':
        db_path = Path('/tmp/courses.db')
    else:
        db_dir = Path('project')
        db_dir.mkdir(exist_ok=True)
        db_path = db_dir / 'courses.db'

    if db_path.exists():
        db_path.unlink()

    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    print(f'📁 База данных: {db_path}\n')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    with UnitOfWork(Session) as uow:
        service = CourseManagementService(uow)

        print_section('1. ДОБАВЛЕНИЕ ДАННЫХ (INSERT)')

        print('\n➕ Добавление преподавателей...')
        teacher1 = service.create_teacher(
            full_name='Dr. Alan Turing',
            department='CS',
            hire_date=date(2020, 1, 15),
            phone='+1-555-0101',
        )
        teacher2 = service.create_teacher(
            full_name='Prof. Ada Lovelace',
            department='Math',
            hire_date=date(2019, 8, 20),
            phone='+1-555-0102',
        )
        uow.commit()
        print('   ✅ Добавлено преподавателей: 2')

        print('\n➕ Добавление курсов...')
        course1 = service.create_course(
            title='Python Programming',
            description='Basics of Python',
            credits=4,
            max_seats=25,
            price=299.0,
            teacher_id=teacher1.id,
        )
        course2 = service.create_course(
            title='SQL for Data Science',
            description='Advanced queries',
            credits=3,
            max_seats=30,
            price=249.0,
            teacher_id=teacher1.id,
        )
        course3 = service.create_course(
            title='Calculus I',
            description='Limits and derivatives',
            credits=5,
            max_seats=35,
            price=349.0,
            teacher_id=teacher2.id,
        )
        uow.commit()
        print('   ✅ Добавлено курсов: 3')

        print('\n➕ Добавление студентов...')
        student1 = service.create_student(
            email='john@example.com', full_name='John Doe', is_active=True
        )
        student2 = service.create_student(
            email='jane@example.com', full_name='Jane Smith', is_active=True
        )
        student3 = service.create_student(
            email='bob@example.com', full_name='Bob Brown', is_active=False
        )
        uow.commit()
        print('   ✅ Добавлено студентов: 3')

        print('\n➕ Запись студентов на курсы...')
        service.enroll_student(student1.id, course1.id)
        service.enroll_student(student1.id, course2.id)
        service.enroll_student(student2.id, course1.id)
        service.enroll_student(student2.id, course3.id)
        service.enroll_student(student3.id, course2.id)
        uow.commit()
        print('   ✅ Создано записей: 5')

        print_section('2. ОБНОВЛЕНИЕ ДАННЫХ (UPDATE)')

        print('\n🔄 Выставление оценок студентам...')
        service.set_grade(student1.id, course1.id, 85.5)
        service.complete_course(student1.id, course1.id)
        service.set_grade(student2.id, course1.id, 92.0)
        service.complete_course(student2.id, course1.id)
        service.set_grade(student2.id, course3.id, 78.0)
        service.complete_course(student2.id, course3.id)
        uow.commit()
        print('   ✅ Оценки выставлены')

        print('\n🔄 Обновление цены курса...')
        old_price = course1.price
        service.update_course_price(course1.id, 349.0)
        uow.commit()
        print(
            f'   ✅ Цена "{course1.title}" изменена: '
            f'{old_price} → {course1.price} руб.'
        )

        print_section('3. ЗАПРОСЫ С WHERE')

        print('\n🔍 Активные студенты:')
        active_students = service.get_active_students_with_courses()
        for student in active_students:
            print(f'   - {student.full_name} ({student.email})')

        print_section('4. ЗАПРОСЫ С JOIN')

        print('\n🔗 Преподаватели и их курсы:')
        teachers = service.get_teachers_with_courses()
        for teacher in teachers:
            print(f'\n   {teacher.full_name} ({teacher.department}):')
            for course in teacher.courses:
                print(
                    f'      📚 {course.title} '
                    f'({course.credits} кредита, {course.price} руб.)'
                )

        print_section('5. ЗАПРОСЫ С GROUP BY')

        print('\n📊 Количество студентов на каждом курсе:')
        course_stats = service.get_students_count_by_course()
        for course, count in course_stats:
            print(f'   {course.title}: {count} студента(ов)')

        print('\n📊 Средняя оценка по курсам:')
        avg_grades = service.get_average_grade_by_course()
        for course, avg_grade in avg_grades:
            print(f'   {course.title}: {avg_grade:.2f}')

        print_section('6. ЗАПРОСЫ С ORDER BY')

        print('\n📈 Топ-3 самых популярных курса:')
        top_courses = service.get_top_popular_courses(3)
        for i, (course, count) in enumerate(top_courses, 1):
            print(f'   {i}. {course.title} — {count} студента(ов)')

        print('\n💰 Курсы, отсортированные по цене (убывание):')
        courses_by_price = service.get_all_courses_ordered_by_price()
        for course in courses_by_price:
            print(f'   {course.title}: {course.price} руб.')

        print_section('7. ЗАПРОСЫ С EXISTS/ANY')

        print('\n🔍 Студенты с незавершёнными курсами:')
        incomplete = service.get_students_with_incomplete_courses()
        for enrollment in incomplete:
            grade_info = (
                f'оценка {enrollment.grade}'
                if enrollment.grade
                else 'оценка не выставлена'
            )
            print(
                f'   - {enrollment.student.full_name}: '
                f'{enrollment.course.title} ({grade_info})'
            )

        print_section('8. УДАЛЕНИЕ ДАННЫХ (DELETE)')

        print('\n🗑️  Удаление студента (каскадное удаление записей)...')
        student_to_delete = student3.full_name
        enrollments_before = len(uow.enrollments.get_all())
        service.delete_student(student3.id)
        uow.commit()
        enrollments_after = len(uow.enrollments.get_all())
        print(f'   ✅ Удалён студент: {student_to_delete}')
        print(
            f'   ✅ Записей до удаления: {enrollments_before}, '
            f'после: {enrollments_after}'
        )

        print('\n🗑️  Удаление преподавателя (в курсах teacher_id = NULL)...')
        teacher_to_delete = teacher2.full_name
        service.delete_teacher(teacher2.id)
        uow.commit()
        print(f'   ✅ Удалён преподаватель: {teacher_to_delete}')

        course_check = uow.courses.get_by_id(course3.id)
        if course_check:
            print(
                f'   ✅ Курс "{course_check.title}" остался, '
                f'teacher_id = {course_check.teacher_id}'
            )

    print('\n' + '=' * 60)
    print('✅ ВСЕ ЗАПРОСЫ ВЫПОЛНЕНЫ УСПЕШНО')
    print('=' * 60)

    if os.name == 'posix' and db_path == Path('/tmp/courses.db'):
        project_db = Path('project/courses.db')
        project_db.parent.mkdir(exist_ok=True)
        shutil.copy2(db_path, project_db)
        print(f'\n📋 База данных скопирована: {project_db}')


if __name__ == '__main__':
    main()
