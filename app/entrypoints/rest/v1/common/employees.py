from fastapi import APIRouter, Request, Query

from app.company import EmployeeResponse, GetEmployeeRequest


employee_router = APIRouter(prefix='/employee')


@employee_router.get('/list', response_model=list[EmployeeResponse])
async def get_list(
    request: Request,
):
    company = request.state.company

    return await company.employees.list()


@employee_router.get('/get/{id_}', response_model=EmployeeResponse)
async def get(
    request: Request,
    id_: str
):
    company = request.state.company

    return await company.employees.get(GetEmployeeRequest(id=id_))
