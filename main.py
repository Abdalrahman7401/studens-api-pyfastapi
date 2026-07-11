import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import mysql.connector
from pydantic import BaseModel
import uvicorn
load_dotenv()
app = FastAPI()

class columnstudent(BaseModel):
    id : int
    name : str
    age : int
    grade : float

class deletstudent(BaseModel):
    id: int

def get_connection():
    host = os.getenv('DB_HOST') or os.getenv('host') or '127.0.0.1'
    user = os.getenv('DB_USER') or os.getenv('user') or 'root'
    password = os.getenv('DB_PASSWORD') or os.getenv('password') or ''
    database = os.getenv('DB_NAME') or os.getenv('database') or ''
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

@app.get("/",include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/students")
async def get_students():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@app.post("/students")
async def post_student(studetsclassdata : columnstudent):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        insertquirey = "INSERT INTO students (id,name,age,grade) VALUES (%s,%s, %s, %s)"
        studentsdata = (studetsclassdata.id,studetsclassdata.name,studetsclassdata.age,studetsclassdata.grade)
        cursor.execute(insertquirey,studentsdata)
        conn.commit()
        conn.close()
        return {"message": "Student Created"}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@app.put("/students")
async def put_student(studetsclassdata : columnstudent):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        insertquirey = "UPDATE students SET name=%s, age=%s, grade=%s WHERE id = %s"
        studentsdata = (studetsclassdata.name,studetsclassdata.age,studetsclassdata.grade, studetsclassdata.id)
        cursor.execute(insertquirey,studentsdata)
        conn.commit()
        conn.close()
        return {"message": "Student Updated"}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@app.delete("/students")
async def delete_student(studetsclassdata : deletstudent):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        insertquirey = "DELETE FROM students WHERE id=%s"
        studentsdata = (studetsclassdata.id,)
        cursor.execute(insertquirey,studentsdata)
        conn.commit()
        conn.close()
        return {"message": "Student Deleted"}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
