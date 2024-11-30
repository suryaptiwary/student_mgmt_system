from fastapi import FastAPI, HTTPException, Path, Query
from bson import ObjectId
from typing import List, Optional

# Import DatabaseConnection from database.py
from database import DatabaseConnection

from models import StudentCreate, StudentUpdate, StudentResponse, Address

app = FastAPI()

# Create database connection
db = DatabaseConnection()

# Define API endpoints

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Student Management API!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.post("/students", response_model=dict, status_code=201)
async def create_student(student: StudentCreate):
    # Convert student to dictionary
    student_dict = student.dict()
    # Insert into MongoDB
    result = db.get_collection().insert_one(student_dict)
    # Return the ID as a string
    return {"id": str(result.inserted_id)}


@app.get("/students", response_model=dict)
async def list_students(
    country: Optional[str] = Query(None),
    age: Optional[int] = Query(None)
):
    query = {}
    if country:
        query['address.country'] = country
    if age is not None:
        query['age'] = {'$gte': age}

    students = list(db.get_collection().find(query))
    for student in students:
        student['id'] = str(student['_id'])
        del student['_id']
    return {"data": students}


@app.get("/students/{id}", response_model=StudentResponse)
async def fetch_student(id: str = Path(..., description="ID of the student")):
    try:
        student = db.get_collection().find_one({"_id": ObjectId(id)})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        student['id'] = str(student['_id'])
        del student['_id']
        return StudentResponse(**student)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid student ID: {str(e)}")


@app.patch("/students/{id}", status_code=204)
async def update_student(
    id: str = Path(..., description="ID of the student to update"),
    student_update: StudentUpdate = None
):
    update_data = {k: v for k, v in student_update.dict().items()
                   if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = db.get_collection().update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")


@app.delete("/students/{id}", status_code=200)
async def delete_student(id: str = Path(...)):
    result = db.get_collection().delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

