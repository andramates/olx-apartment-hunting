from src.application.ports.user_repository import UserRepository
from src.domain.entities.user import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, name: str, email: str) -> User:
        existing_user = self.user_repository.get_by_email(email)
        if existing_user is not None:
            raise ValueError("User with this email already exists")

        user = User(
            id=None,
            name=name,
            email=email,
        )
        return self.user_repository.add(user)

    def get_user(self, user_id: int) -> User | None:
        return self.user_repository.get_by_id(user_id)

    def list_users(self) -> list[User]:
        return self.user_repository.list_all()