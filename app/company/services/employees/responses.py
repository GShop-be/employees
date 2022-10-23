from pydantic import BaseModel, EmailStr


__all__ = [
    'EmployeeResponse'
]


class EmployeeResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
