"""Модели данных для системы управления онлайн-курсами."""

from datetime import date, datetime

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс для всех моделей ORM."""

    pass


class Student(Base):
    """Модель студента онлайн-школы.

    Attributes:
        id: Уникальный идентификатор студента
        email: Адрес электронной почты (логин)
        full_name: Полное имя студента
        enrolled_at: Дата и время регистрации
        is_active: Статус активности (True - активен, False - заблокирован)
        enrollments: Список записей студента на курсы
    """

    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    enrolled_at: Mapped[datetime] = mapped_column(
        default=datetime.now, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    enrollments: Mapped[list['Enrollment']] = relationship(
        back_populates='student', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление студента.

        Returns:
            Строка с информацией о студенте
        """
        return (
            f"Student(id={self.id}, email='{self.email}', "
            f"full_name='{self.full_name}', is_active={self.is_active})"
        )


class Teacher(Base):
    """Модель преподавателя.

    Attributes:
        id: Уникальный идентификатор преподавателя
        full_name: Полное имя преподавателя
        department: Название кафедры
        hire_date: Дата найма на работу
        phone: Номер телефона
        courses: Список курсов, которые ведёт преподаватель
    """

    __tablename__ = 'teachers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    department: Mapped[str] = mapped_column(String, nullable=False)
    hire_date: Mapped[date | None] = mapped_column()
    phone: Mapped[str | None] = mapped_column(String(15), unique=True)

    courses: Mapped[list['Course']] = relationship(
        back_populates='teacher'
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление преподавателя.

        Returns:
            Строка с информацией о преподавателе
        """
        return (
            f"Teacher(id={self.id}, full_name='{self.full_name}', "
            f"department='{self.department}')"
        )


class Course(Base):
    """Модель учебного курса.

    Attributes:
        id: Уникальный идентификатор курса
        title: Название курса
        description: Подробное описание курса
        credits: Количество кредитных часов
        max_seats: Максимальное количество студентов
        price: Стоимость курса в рублях
        teacher_id: ID преподавателя, ведущего курс
        teacher: Объект преподавателя
        enrollments: Список записей студентов на курс
    """

    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    credits: Mapped[int] = mapped_column(default=3, nullable=False)
    max_seats: Mapped[int] = mapped_column(default=30, nullable=False)
    price: Mapped[float] = mapped_column(default=0.0, nullable=False)
    teacher_id: Mapped[int | None] = mapped_column(
        ForeignKey('teachers.id', ondelete='SET NULL')
    )

    teacher: Mapped['Teacher | None'] = relationship(back_populates='courses')
    enrollments: Mapped[list['Enrollment']] = relationship(
        back_populates='course', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление курса.

        Returns:
            Строка с информацией о курсе
        """
        return (
            f"Course(id={self.id}, title='{self.title}', "
            f"credits={self.credits}, price={self.price})"
        )


class Enrollment(Base):
    """Модель записи студента на курс (связь many-to-many).

    Attributes:
        student_id: ID студента
        course_id: ID курса
        enrolled_at: Дата и время записи на курс
        grade: Оценка за курс (0-100, None если не выставлена)
        is_completed: Флаг завершения курса
        student: Объект студента
        course: Объект курса
    """

    __tablename__ = 'enrollments'

    student_id: Mapped[int] = mapped_column(
        ForeignKey('students.id', ondelete='CASCADE'), primary_key=True
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey('courses.id', ondelete='CASCADE'), primary_key=True
    )
    enrolled_at: Mapped[datetime] = mapped_column(
        default=datetime.now, nullable=False
    )
    grade: Mapped[float | None] = mapped_column()
    is_completed: Mapped[bool] = mapped_column(
        default=False, nullable=False
    )

    student: Mapped['Student'] = relationship(back_populates='enrollments')
    course: Mapped['Course'] = relationship(back_populates='enrollments')

    def __repr__(self) -> str:
        """Возвращает строковое представление записи.

        Returns:
            Строка с информацией о записи
        """
        return (
            f'Enrollment(student_id={self.student_id}, '
            f'course_id={self.course_id}, grade={self.grade}, '
            f'is_completed={self.is_completed})'
        )
