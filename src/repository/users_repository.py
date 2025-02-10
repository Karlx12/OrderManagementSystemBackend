from typing import Optional, List
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session
from ..models.users import User, RefreshToken
from datetime import datetime, timedelta


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        return self.session.scalar(
            select(User).where(User.username == username)
        )

    def get_by_employee_dni(self, employee_dni: str) -> Optional[User]:
        return self.session.scalar(
            select(User).where(User.employee_dni == employee_dni)
        )

    def get_all(self) -> List[User]:
        return list(self.session.scalars(select(User)))

    def get_active(self) -> List[User]:
        return list(
            self.session.scalars(select(User).where(User.is_active is False))
        )

    def update(self, user: User) -> User:
        self.session.merge(user)
        self.session.commit()
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()

    def register_failed_attempt(self, user: User) -> User:
        user.failed_attempts += 1
        if user.failed_attempts >= 3:
            user.blocked_until = datetime.now(
                datetime.timezone.utc
            ) + timedelta(minutes=15)
        self.session.commit()
        return user

    def reset_failed_attempts(self, user: User) -> User:
        user.failed_attempts = 0
        user.blocked_until = None
        user.last_login = datetime.now(datetime.timezone.utc)
        self.session.commit()
        return user

    def create_refresh_token(
        self,
        user_id: int,
        token_hash: str,
        device: str = None,
        ip: str = None,
        user_agent: str = None,
    ) -> RefreshToken:
        token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=datetime.now(datetime.timezone.utc) + timedelta(days=7),
            device=device,
            ip_address=ip,
            user_agent=user_agent,
        )
        self.session.add(token)
        self.session.commit()
        return token

    def get_valid_token(self, token_hash: str) -> Optional[RefreshToken]:
        return self.session.scalar(
            select(RefreshToken).where(
                and_(
                    RefreshToken.token_hash == token_hash,
                    RefreshToken.expires_at
                    > datetime.now(datetime.timezone.utc),
                    RefreshToken.is_revoked is False,
                )
            )
        )

    def revoke_all_tokens(self, user_id: int) -> None:
        self.session.query(RefreshToken).filter(
            RefreshToken.user_id == user_id
        ).update({RefreshToken.is_revoked: True})
        self.session.commit()

    def clean_expired_tokens(self) -> None:
        self.session.query(RefreshToken).filter(
            or_(
                RefreshToken.expires_at < datetime.now(datetime.timezone.utc),
                RefreshToken.is_revoked is False,
            )
        ).delete()
        self.session.commit()

    def update_last_activity(self, user: User) -> None:
        user.last_activity = datetime.now(datetime.timezone.utc)
        self.session.commit()

    def soft_delete(self, user: User) -> None:
        user.is_deleted = True
        user.is_active = False
        self.revoke_all_tokens(user.id)
        self.session.commit()
