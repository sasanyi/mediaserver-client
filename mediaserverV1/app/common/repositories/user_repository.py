from typing import List, Optional
from app.app import db
from app.common.models.user import User


class UserRepository:

    def create_user(self, user: User):
        self._save_changes(user)

    def get_all_users(self) -> List[User]:
        return User.query.all()

    def get_user_by_id(self, public_id: str) -> Optional[User]:
        return User.query.filter_by(public_id=public_id).first()

    def get_user_by_email(self, email: str) -> User:
        return User.query.filter_by(email=email).first()

    def _save_changes(self, data: User):
        db.session.add(data)
        db.session.commit()
