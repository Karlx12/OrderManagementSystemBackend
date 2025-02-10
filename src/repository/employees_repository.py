from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models.employees import Employee
from ..models.enums import UserRole, EmployeeStatus


class EmployeeRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, employee: Employee) -> Employee:
        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        return employee

    def get_by_dni(self, dni: str) -> Optional[Employee]:
        return self.session.get(Employee, dni)

    def get_by_role(self, role: UserRole) -> List[Employee]:
        return list(
            self.session.scalars(select(Employee).where(Employee.role == role))
        )

    def get_all(self) -> List[Employee]:
        return list(self.session.scalars(select(Employee)))

    def get_active(self) -> List[Employee]:
        return list(
            self.session.scalars(
                select(Employee).where(
                    Employee.status == EmployeeStatus.ACTIVE
                )
            )
        )

    def update(self, employee: Employee) -> Employee:
        self.session.merge(employee)
        self.session.commit()
        return employee

    def delete(self, employee: Employee) -> None:
        self.session.delete(employee)
        self.session.commit()
