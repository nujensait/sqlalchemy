"""Репозитории для работы с моделями данных."""

from project.repositories.base_repository import BaseRepository
from project.repositories.course_repository import CourseRepository
from project.repositories.enrollment_repository import EnrollmentRepository
from project.repositories.student_repository import StudentRepository
from project.repositories.teacher_repository import TeacherRepository

__all__ = [
    'BaseRepository',
    'StudentRepository',
    'TeacherRepository',
    'CourseRepository',
    'EnrollmentRepository',
]
