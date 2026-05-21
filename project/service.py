"""Сервисный слой для бизнес-логики системы управления курсами."""

from datetime import date, datetime

from project.models import Course, Enrollment, Student, Teacher
from project.unit_of_work import UnitOfWork


class CourseManagementService:
    """Сервис для управления онлайн-курсами.

    Attributes:
        uow: Unit of Work для работы с репозиториями
    """

    def __init__(self, uow: UnitOfWork) -> None:
        """Инициализирует сервис.

        Args:
            uow: Unit of Work
        """
        self.uow = uow

    def create_student(
        self, email: str, full_name: str, is_active: bool = True
    ) -> Student:
        """Создаёт нового студента.

        Args:
            email: Email студента
            full_name: Полное имя
            is_active: Статус активности

        Returns:
            Созданный студент
        """
        student = Student(
            email=email, full_name=full_name, is_active=is_active
        )
        return self.uow.students.add(student)

    def create_teacher(
        self,
        full_name: str,
        department: str,
        hire_date: date | None = None,
        phone: str | None = None,
    ) -> Teacher:
        """Создаёт нового преподавателя.

        Args:
            full_name: Полное имя
            department: Кафедра
            hire_date: Дата найма
            phone: Телефон

        Returns:
            Созданный преподаватель
        """
        teacher = Teacher(
            full_name=full_name,
            department=department,
            hire_date=hire_date,
            phone=phone,
        )
        return self.uow.teachers.add(teacher)

    def create_course(
        self,
        title: str,
        teacher_id: int,
        description: str | None = None,
        credits: int = 3,
        max_seats: int = 30,
        price: float = 0.0,
    ) -> Course:
        """Создаёт новый курс.

        Args:
            title: Название курса
            teacher_id: ID преподавателя
            description: Описание
            credits: Кредиты
            max_seats: Максимум мест
            price: Цена

        Returns:
            Созданный курс
        """
        course = Course(
            title=title,
            teacher_id=teacher_id,
            description=description,
            credits=credits,
            max_seats=max_seats,
            price=price,
        )
        return self.uow.courses.add(course)

    def enroll_student(
        self, student_id: int, course_id: int
    ) -> Enrollment:
        """Записывает студента на курс.

        Args:
            student_id: ID студента
            course_id: ID курса

        Returns:
            Созданная запись
        """
        enrollment = Enrollment(student_id=student_id, course_id=course_id)
        return self.uow.enrollments.add(enrollment)

    def set_grade(
        self, student_id: int, course_id: int, grade: float
    ) -> Enrollment | None:
        """Выставляет оценку студенту за курс.

        Args:
            student_id: ID студента
            course_id: ID курса
            grade: Оценка (0-100)

        Returns:
            Обновлённая запись или None
        """
        enrollment = self.uow.enrollments.get_by_student_and_course(
            student_id, course_id
        )
        if enrollment:
            enrollment.grade = grade
            return self.uow.enrollments.update(enrollment)
        return None

    def complete_course(
        self, student_id: int, course_id: int
    ) -> Enrollment | None:
        """Отмечает курс как завершённый.

        Args:
            student_id: ID студента
            course_id: ID курса

        Returns:
            Обновлённая запись или None
        """
        enrollment = self.uow.enrollments.get_by_student_and_course(
            student_id, course_id
        )
        if enrollment:
            enrollment.is_completed = True
            return self.uow.enrollments.update(enrollment)
        return None

    def update_course_price(
        self, course_id: int, new_price: float
    ) -> Course | None:
        """Обновляет цену курса.

        Args:
            course_id: ID курса
            new_price: Новая цена

        Returns:
            Обновлённый курс или None
        """
        course = self.uow.courses.get_by_id(course_id)
        if course:
            course.price = new_price
            return self.uow.courses.update(course)
        return None

    def deactivate_student(self, student_id: int) -> Student | None:
        """Деактивирует студента.

        Args:
            student_id: ID студента

        Returns:
            Обновлённый студент или None
        """
        student = self.uow.students.get_by_id(student_id)
        if student:
            student.is_active = False
            return self.uow.students.update(student)
        return None

    def delete_student(self, student_id: int) -> None:
        """Удаляет студента (каскадно удаляются его записи).

        Args:
            student_id: ID студента
        """
        student = self.uow.students.get_by_id(student_id)
        if student:
            self.uow.students.delete(student)

    def delete_course(self, course_id: int) -> None:
        """Удаляет курс (каскадно удаляются записи студентов).

        Args:
            course_id: ID курса
        """
        course = self.uow.courses.get_by_id(course_id)
        if course:
            self.uow.courses.delete(course)

    def delete_teacher(self, teacher_id: int) -> None:
        """Удаляет преподавателя (в курсах teacher_id = NULL).

        Args:
            teacher_id: ID преподавателя
        """
        teacher = self.uow.teachers.get_by_id(teacher_id)
        if teacher:
            self.uow.teachers.delete(teacher)

    def get_top_popular_courses(self, limit: int = 3) -> list[tuple]:
        """Получает топ популярных курсов.

        Args:
            limit: Количество курсов

        Returns:
            Список кортежей (course, count)
        """
        return self.uow.courses.get_top_popular_courses(limit)

    def get_active_students_with_courses(self) -> list[Student]:
        """Получает активных студентов с их курсами.

        Returns:
            Список активных студентов
        """
        return self.uow.students.get_active_students()

    def get_teachers_with_courses(self) -> list[Teacher]:
        """Получает всех преподавателей с их курсами.

        Returns:
            Список преподавателей с курсами
        """
        return self.uow.teachers.get_all_with_courses()

    def get_students_with_incomplete_courses(self) -> list[Enrollment]:
        """Получает студентов с незавершёнными курсами.

        Returns:
            Список незавершённых записей
        """
        return self.uow.enrollments.get_incomplete_enrollments()

    def get_students_count_by_course(self) -> list[tuple]:
        """Получает количество студентов на каждом курсе.

        Returns:
            Список кортежей (course, count)
        """
        return self.uow.enrollments.get_students_count_by_course()

    def get_average_grade_by_course(self) -> list[tuple]:
        """Получает среднюю оценку по каждому курсу.

        Returns:
            Список кортежей (course, avg_grade)
        """
        return self.uow.enrollments.get_average_grade_by_course()

    def get_all_courses_ordered_by_price(self) -> list[Course]:
        """Получает все курсы, отсортированные по цене.

        Returns:
            Список курсов
        """
        return self.uow.courses.get_all_ordered_by_price()
