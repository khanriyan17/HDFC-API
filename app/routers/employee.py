from typing import List

from fastapi import APIRouter

from app.dataaccess import database
from app.models.employee import Employee, EmployeeCreate, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=List[Employee])
def get_employees():
    return database.fetch_all("SELECT * FROM employee")


@router.get("/{empId}", response_model=Employee)
def get_employee(empId: int):
    return database.fetch_one("SELECT * FROM employee WHERE empId = %s", (empId,))


@router.post("/", response_model=Employee, status_code=201)
def create_employee(employee: EmployeeCreate):
    new_id = database.execute(
        "INSERT INTO employee (firstname, surname, job, phoneno, emailid, education, state, dob, joindate) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            employee.firstname,
            employee.surname,
            employee.job,
            employee.phoneno,
            employee.emailId,
            employee.education,
            employee.state,
            employee.dob,
            employee.joindate,
        ),
    )
    return database.fetch_one("SELECT * FROM employee WHERE empId = %s", (new_id,))


@router.put("/{empId}", response_model=Employee)
def update_employee(empId: int, employee: EmployeeUpdate):
    database.execute(
        "UPDATE employee SET firstname=%s, surname=%s, job=%s, phoneno=%s, emailid=%s, "
        "education=%s, state=%s, dob=%s, joindate=%s WHERE EmpId=%s",
        (
            employee.firstname,
            employee.surname,
            employee.job,
            employee.phoneno,
            employee.emailId,
            employee.education,
            employee.state,
            employee.dob,
            employee.joindate,
            empId,
        ),
    )
    return database.fetch_one("SELECT * FROM employee WHERE empId = %s", (empId,))


@router.delete("/{empId}", status_code=204)
def delete_employee(empId: int):
    database.execute("DELETE FROM employee WHERE empId = %s", (empId,))