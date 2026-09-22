from typing import List

from fastapi import APIRouter

from app.dataaccess import database
from app.models.user import User, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
def get_users():
    return database.fetch_all("SELECT * FROM users")


@router.get("/{userId}", response_model=User)
def get_users(userId:int):
    return database.fetch_one("SELECT * FROM users WHERE userId = %s", (userId,))


@router.post("/", response_model=User, status_code=201)
def create_user(user: UserCreate):
    new_id = database.execute(
        "INSERT INTO users (firstname, lastname, phoneno, emailid, username, password, createddate, lastlogin) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (
            user.firstname,
            user.lastname,
            user.phoneno,
            user.emailId,
            user.username,
            user.password,
            user.createddate,
            user.lastlogin,
        ),
    )
    return database.fetch_one("SELECT * FROM employee WHERE empId = %s", (new_id,))


@router.put("/{userId}", response_model=User)
def update_employee(userId: int, user: UserUpdate):
    database.execute(
        "UPDATE users SET firstname=%s, lastname=%s, phoneno=%s, emailid=%s, "
         " username=%s, password=%s, createddate=%s, lastlogin=%s WHERE userId=%s",
        (
            user.firstname,
            user.lastname,
            user.phoneno,
            user.emailId,
            user.username,
            user.password,
            user.createddate,
            user.lastlogin,
            userId,
        ),
    )
    return database.fetch_one("SELECT * FROM users WHERE userId = %s", (userId,))


@router.delete("/{userId}", status_code=204)
def delete_user(userId: int):
    database.execute("DELETE FROM employee WHERE EmpId = %s", (userId,))