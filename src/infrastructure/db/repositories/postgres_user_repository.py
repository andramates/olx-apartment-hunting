from sqlalchemy.orm import Session

from src.application.ports.user_repository import UserRepository
from src.domain.entities.user import User
from src.infrastructure.db.models.user_model import UserModel


class PostgresUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> User:
        user_model = UserModel(
            name=user.name,
            email=user.email,
        )
        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)

        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            created_at=user_model.created_at,
        )

    def get_by_id(self, user_id: int) -> User | None:
        user_model = self.session.get(UserModel, user_id)
        if user_model is None:
            return None

        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            created_at=user_model.created_at,
        )

    def get_by_email(self, email: str) -> User | None:
        user_model = (
            self.session.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )
        if user_model is None:
            return None

        return User(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            created_at=user_model.created_at,
        )

    def list_all(self) -> list[User]:
        user_models = self.session.query(UserModel).all()

        return [
            User(
                id=user_model.id,
                name=user_model.name,
                email=user_model.email,
                created_at=user_model.created_at,
            )
            for user_model in user_models
        ]