from typing import Optional, Any

from pydantic import BaseModel, EmailStr, validator


__all__ = [
    'NewEmployeeRequest',
    'UpdateEmployeeRequest',
    'DeleteEmployeeRequest',
    'GetEmployeeRequest'
]


class GetEmployeeRequest(BaseModel):
    id: str


class NewEmployeeRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    repeated_password: str
    role: str


class EmployeeFields(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str]
    password: Optional[str]
    repeated_password: Optional[str]

    @validator('password')
    def password_match(cls, v: str, values: dict[str, Any], **kwargs):
        if (
            'password' in values and 'repeated_password' not in values
            or 'password' not in values and 'repeated_password' in values
        ):
            raise ValueError('You must provide password and repeated password if you want to update it.')

        if 'password' in values and v != values['password1']:
            raise ValueError('Passwords must match.')
        return v


class UpdateEmployeeRequest(BaseModel):
    id: str
    fields: EmployeeFields


class DeleteEmployeeRequest(BaseModel):
    id: str
