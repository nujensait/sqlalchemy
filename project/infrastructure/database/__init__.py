"""Модели базы данных."""

from project.infrastructure.database.base import Base
from project.infrastructure.database.course import Course
from project.infrastructure.database.enrollment import Enrollment
from project.infrastructure.database.student import Student
from project.infrastructure.database.teacher import Teacher

__all__ = ['Base', 'Student', 'Teacher', 'Course', 'Enrollment']
