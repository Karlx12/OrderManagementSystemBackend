from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.clients import Client


class ClientRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, client: Client) -> Client:
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

    def get_by_dni(self, dni: str) -> Optional[Client]:
        return self.session.get(Client, dni)

    def get_all(self) -> List[Client]:
        return list(self.session.scalars(select(Client)))

    def update(self, client: Client) -> Client:
        self.session.merge(client)
        self.session.commit()
        return client

    def delete(self, client: Client) -> None:
        self.session.delete(client)
        self.session.commit()
