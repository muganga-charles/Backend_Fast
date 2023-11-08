from fastapi import FastAPI, HTTPException
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from fastapi.responses import JSONResponse

# import bcrypt
# from bcrypt import hashpw, gensalt, checkpw
import numpy as np

# from email_module import Email
# from fastapi import BackgroundTasks
import config
from fastapi.middleware.cors import CORSMiddleware
from py_functions import (
    Patient,
    LoginData,
    Hospital,
    Doctor,
    DoctorLoginData,
    HospitalDoctor,
    hash_password,
    verify_password,
)

import py_functions

app = FastAPI()
# origins = (["*"],)
# app.add_middleware(
#     CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def connect_db():
    server = config.SERVER_NAME
    database = config.DATABASE_NAME
    user = config.USER
    password = config.PASSWORD
    con_string = f"dbname='{database}' user='{user}' host='{server}' password='{password}' sslmode='require'"

    cnxn = psycopg2.connect(con_string)
    cnxn.autocommit = True
    cursor = cnxn.cursor()
    print("Connected to database")
    return cnxn


cnxn = connect_db()


@app.get("/")
def get_data():
    data, columns = py_functions.fetch_data(cnxn)
    # Convert list of tuples to list of dictionaries
    return [dict(zip(columns, record)) for record in data]


@app.post("/login")
async def login(login_data: LoginData):
    patient = py_functions.fetch_patient_by_email(cnxn, login_data.email)
    if not patient:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # The 'password' field in the patient record should contain the hashed password
    if not verify_password(patient["password"], login_data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # If the password is correct, proceed with login success logic
    return {"success": True, "message": "Login successful."}


@app.post("/patients/new")
async def create_patient(patient_data: Patient):
    existing_patient = py_functions.existing_patient(
        cnxn, patient_data.email, patient_data.referral_no
    )
    if existing_patient:
        raise HTTPException(status_code=400, detail="User already exists.")

    hashed_password = hash_password(patient_data.password)
    patient_data.password = hashed_password

    py_functions.store_patient(cnxn, patient_data)

    return {"success": True, "message": "User added successfully."}


# @app.post("/patients/new")
# async def create_patient(patient: Patient):
#     # Check if the user exists
#     existing_client = py_functions.existing_patient(
#         cnxn, patient.email, patient.referral_no
#     )
#     if existing_client:
#         raise HTTPException(status_code=400, detail="User already exists.")

#     # salt_rounds = 12
#     hashed_password = hash_password(patient.password)
#     # hashed_password = ""
#     # Create a new patient with the hashed password
#     patient.password = hashed_password

#     py_functions.store_patient(cnxn, patient)

#     # Send welcome email
#     # if patient.name:
#     #     await Email(patient.email, "Welcome").send_welcome(patient.name)
#     return JSONResponse(
#         status_code=200,
#         content={
#             "success": True,
#             "message": "User added successfully.",
#             "data": {"added": True},
#         },
#     )


# @app.post("/login")
# async def login(login_data: LoginData):
#     patient = py_functions.fetch_patient_by_email(cnxn, login_data.email)
#     if not patient:
#         raise HTTPException(status_code=401, detail="Invalid email or password.")

#     # The 'password' field in the patient record should contain the hashed password
#     if not verify_password(patient["password"], login_data.password):
#         raise HTTPException(status_code=401, detail="Invalid email or password.")

#     # If the password is correct, proceed with login success logic
#     # For example, you could generate and return a token for the session
#     return {"success": True, "message": "Login successful."}


# @app.post("/login")
# async def login(login_data: LoginData):
#     # Fetch the patient data from the database using the provided email
#     patient = py_functions.fetch_patient_by_email(cnxn, login_data.email)
#     password = login_data.password.encode("utf-8")
#     hashed_password = patient["password"]
#     if isinstance(hashed_password, str):
#         hashed_password = hashed_password.encode("utf-8")
#     if not patient or verify_password(hashed_password, password):
#         raise HTTPException(status_code=401, detail="Invalid email or password.")

#     # If everything is okay, return a success message
#     return {
#         "success": True,
#         "message": "Login successful.",
#         "data": {"name": patient["name"]},
#     }


@app.post("/hospitals/new")
async def create_hospital(hospital: Hospital):
    # Check if the user exists
    existing_client = py_functions.existing_hospital(cnxn, hospital.Email)
    if existing_client:
        raise HTTPException(status_code=400, detail="Hospital already exists.")

    py_functions.add_hospital(cnxn, hospital)

    # Send welcome email
    # if patient.name:
    #     await Email(patient.email, "Welcome").send_welcome(patient.name)

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "Hospital added successfully.",
            "data": {"added": True},
        },
    )


@app.post("/doctors/new")
async def create_doctor(doctor: Doctor):
    # Check if the user exists
    existing_client = py_functions.existing_doctor(cnxn, doctor.Email)
    if existing_client:
        raise HTTPException(status_code=400, detail="doctor already exists.")

    salt_rounds = 12
    hashed_password = ""
    # hashed_password = hashpw(doctor.Password.encode("utf-8"), gensalt(salt_rounds))
    doctor.Password = hashed_password

    py_functions.add_doctor(cnxn, doctor)

    # Send welcome email
    # if patient.name:
    #     await Email(patient.email, "Welcome").send_welcome(patient.name)

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "doctor added successfully.",
            "data": {"added": True},
        },
    )


# @app.post("/doctors/login")
# async def doctor_login(login_data: DoctorLoginData):
#     # Fetch the patient data from the database using the provided email
#     doctor = py_functions.fetch_doctor_by_email(cnxn, login_data.Email)
#     # print(patient['password'])
#     # If the patient doesn't exist or passwords don't match, return an error
#     # if not doctor(
#     if not doctor or not checkpw(
#         login_data.Password.encode("utf-8"), doctor["Password"].encode("utf-8")
#     ):
#         raise HTTPException(status_code=401, detail="Invalid email or password.")

#     return {
#         "success": True,
#         "message": "Login successful.",
#         "data": {"name": doctor["DoctorName"]},
#     }


# # @app.post("/doctor-to-hospital")
# # async def doctor_to_hospital(hospital_doctor: HospitalDoctor):
# #     try:
# #         py_functions.add_hospital_doctor(cnxn, hospital_doctor)
# #         return {"success": True, "message": "Doctor assigned to hospital successfully."}
# #     except Exception as e:
# #         raise HTTPException(status_code=400, detail=str(e))


@app.get("/patient_data")
def get_patient_data():
    df = py_functions.fetch_patient_data(cnxn)
    df.replace([np.inf, -np.inf], None, inplace=True)  # Replace infinities with None
    df = df.where(pd.notnull(df), None)  # Replace NaNs with None
    return df.to_dict(orient="records")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
