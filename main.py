from fastapi import FastAPI, HTTPException, status, Path
from .db.main import get_db, init_db
from .models import User, Login, Del



app = FastAPI(title="Vun",
              description="project in ehucal hacking")


@app.on_event("startup")
def init():
    init_db()

@app.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_student(user: User):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"INSERT INTO users (username, email, password) VALUES ('{user.username}', '{user.email}', '{user.password}')")
        conn.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")
    finally:
        conn.close()

@app.get("/users", status_code=status.HTTP_200_OK)
def get_all_users():
    conn = get_db()
    cursor = conn.cursor()
    results = cursor.execute(f"SELECT * FROM users")
    rows = results.fetchall()
    conn.close()

    if not rows:
        return {"message": "No user records found"}

    return [dict(row) for row in rows]



@app.post("/login_user", status_code=status.HTTP_200_OK)
def login_user(data: Login):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"SELECT * FROM users WHERE email = '{data.email}' AND password = '{data.password}'")
        result = cursor.fetchone()

        if not result:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "User doesn't exist"})

        return {"message": "user logged in succesfully", "data": result}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")

@app.delete("/students/{id}", status_code=status.HTTP_200_OK)
def delete_students(id: int = Path(...), confirm: bool = False):
    conn = get_db()
    cursor = conn.cursor()
    if not confirm:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Delete terminated")
    cursor.execute(
        f"DELETE FROM users WHERE id = '{id}'"
    )
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}


