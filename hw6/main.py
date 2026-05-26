from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lesson_6.infrastructure.database.unit_of_work import UnitOfWork
from lesson_6.service.user_service import UserService

# Настройка
engine = create_engine('sqlite+pysqlite:///mydb.db', echo=False)
Session = sessionmaker(bind=engine)


def main():
    # Создаем UOW
    with UnitOfWork(Session) as uow:
        # Создаем сервис
        user_service = UserService(uow)

        print('=' * 60)
        print('📊 ТОП-3 ПОПУЛЯРНЫЕ КНИГИ')
        print('=' * 60)

        top_books = user_service.get_top_books(3)
        for i, (id, title, author, count) in enumerate(top_books, 1):
            print(f'{i}. {title} - {author} (читают {count} пользователей)')

        print('\n' + '=' * 60)
        print('👥 ПОЛЬЗОВАТЕЛИ С КНИГАМИ')
        print('=' * 60)

        users = user_service.get_all_users_with_books_efficient()
        for user in users:
            print(f'\n{user["name"]}: {user["books_count"]} книг(и)')
            for book in user['books']:
                print(f'    📖 {book}')

        print('\n' + '=' * 60)
        print('🔍 ДЕТАЛЬНЫЙ ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ')
        print('=' * 60)

        # Получаем пользователя 1 (ivan)
        user_detail = user_service.get_user_with_books(1)
        print(f'👤 {user_detail["fullname"]} (@{user_detail["name"]})')
        print('Книги:')
        for book in user_detail['books']:
            print(f'    📖 {book["title"]} - {book["author"]}')


if __name__ == '__main__':
    main()
