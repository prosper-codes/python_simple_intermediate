from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from typing import Optional

app = FastAPI()

# Enable CORS so the HTML frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        dbname="student_db",
        user="postgres",
        password="qwerty123",
        host="localhost",
        port="5433"
    )
    return conn

# Pydantic model for student data
class Student(BaseModel):
    name: str
    address: str
    age: int
    number: str

class StudentUpdate(BaseModel):
    student_id: int
    name: str
    address: str
    age: int
    number: str

# Create table endpoint
@app.post("/create-table")
def create_table():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students(
                student_id SERIAL PRIMARY KEY,
                name TEXT,
                address TEXT,
                age INT,
                number TEXT
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Table created successfully"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get all students
@app.get("/students")
def get_students():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students ORDER BY student_id;")
        records = cur.fetchall()
        cur.close()
        conn.close()
        
        students = []
        for record in records:
            students.append({
                "student_id": record[0],
                "name": record[1],
                "address": record[2],
                "age": record[3],
                "number": record[4]
            })
        return students
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Insert student
@app.post("/students")
def insert_student(student: Student):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students(name, address, age, number) VALUES (%s, %s, %s, %s)",
            (student.name, student.address, student.age, student.number)
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Data inserted successfully"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update student
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE students SET name = %s, address = %s, age = %s, number = %s WHERE student_id = %s",
            (student.name, student.address, student.age, student.number, student_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Data updated successfully"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Data deleted successfully"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)