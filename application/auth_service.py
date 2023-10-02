from sqlmodel import Session, select
from persistence.db_utils import get_engine
from presentation.models.viewmodels import UserCreate, User


class AuthRepository:

    def __init__(self):
        self.session = Session(get_engine())

    def save(self, user: UserCreate):
        user_created = User.from_user_create(user)
        self.session.add(user_created)
        self.session.commit()
        self.session.refresh(user_created)
        self.session.close()
        return user_created

    def get_user_by_login(self, login: str):
        sttm = select(User).where(User.login == login)
        user = self.session.exec(sttm).first()
        self.session.close()
        return user
    
    