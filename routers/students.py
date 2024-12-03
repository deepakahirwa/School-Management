from fastapi import APIRouter, HTTPException
from model import StudentModel, StudentResponse
from database import students_collection
from bson import ObjectId

router = APIRouter(prefix="/api/students", tags=["students"])

# Create Student
@router.post("/", response_model=StudentResponse)
async def create_student(student: StudentModel):
    student_data = student.dict()
    result = await students_collection.insert_one(student_data)
    created_student = {
        "id": str(result.inserted_id),
        **student_data,
    }
    return created_student

# List Students
@router.get("/")
async def list_students():
    try:
        students = await students_collection.find().to_list(100)
        for student in students:
            student["id"] = str(student.pop("_id"))
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving students: {str(e)}")

# Fetch Student by ID
@router.get("/{id}", response_model=StudentResponse)
async def fetch_student(id: str):
    try:
        student = await students_collection.find_one({"_id": ObjectId(id)})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        student["id"] = str(student.pop("_id"))
        return student
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving student: {str(e)}")



@router.patch("/{id}")
async def update_student(id: str, student: StudentModel):
    try:
        # Check if the student exists
        print(id, student)
        existing_student = await students_collection.find_one({"_id": ObjectId(id)})
        print(existing_student)

        if not existing_student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Prepare the data for updating (exclude unset fields)
        student_data = student.model_dump(exclude_unset=True)

        # Proceed with the update
        update_result = await students_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": student_data}
        )

        # Check if the student was actually updated
        if update_result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Student data was not updated")

        return {"message": "Student updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating student: {str(e)}")




# Delete Student
@router.delete("/{id}")
async def delete_student(id: str):
    try:
        delete_result = await students_collection.delete_one({"_id": ObjectId(id)})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting student: {str(e)}")
