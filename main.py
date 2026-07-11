import os
from dotenv import dotenv_values,load_dotenv
from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class columnstudent(BaseModel):
    id : int
    name : str
    age : int
    grade : float

class deletstudent(BaseModel):
    id: int

def get_connection():
    return mysql.connector.connect(
        host=os.getenv('host'),
        user=os.getenv('host'),
        password=os.getenv('host'),
        database=os.getenv('host')
    )



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
        cursor = conn.cursor(dictionary=True)
        insertquirey = "INSERT INTO students (id,name,age,grade) VALUES (%s,%s, %s, %s)"
        studentsdata = (studetsclassdata.id,studetsclassdata.name,studetsclassdata.age,studetsclassdata.grade)
        cursor.execute(insertquirey,studentsdata)
        conn.commit()
        conn.close()
        return "Student Created"
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@app.put("/students")
async def put_student(studetsclassdata : columnstudent):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        insertquirey = "UPDATE students SET name=%s, age=%s, grade=%s WHERE id = %s"
        studentsdata = (studetsclassdata.name,studetsclassdata.age,studetsclassdata.grade, studetsclassdata.id)
        cursor.execute(insertquirey,studentsdata)
        conn.commit()
        conn.close()
        return "Student Updated"
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@app.delete("/students")
async def delete_student(studetsclassdata : deletstudent):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        insertquirey = "DELETE FROM students WHERE id=%s"
        studentsdata = (studetsclassdata.id,)
        cursor.execute(insertquirey,studentsdata)
        conn.commit()
        conn.close()
        return "Student Deleted"
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)


