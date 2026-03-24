from src.infrastructure.db.session import SessionLocal
from src.infrastructure.db.repositories.postgres_user_repository import PostgresUserRepository
from src.infrastructure.db.repositories.postgres_filter_repository import PostgresFilterRepository
from src.application.services.user_service import UserService
from src.application.services.filter_service import FilterService


def main():
    session = SessionLocal()

    user_repository = PostgresUserRepository(session)
    filter_repository = PostgresFilterRepository(session)

    user_service = UserService(user_repository)
    filter_service = FilterService(filter_repository, user_repository)

    user = user_service.create_user("Andra", "andra@example.com")
    print(user)

    search_filter = filter_service.create_filter(
        user_id=user.id,
        name="2 camere Cluj",
        olx_url="https://www.olx.ro/",
        check_interval_minutes=5,
    )
    print(search_filter)

    filters = filter_service.list_user_filters(user.id)
    print(filters)

    session.close()


if __name__ == "__main__":
    main()