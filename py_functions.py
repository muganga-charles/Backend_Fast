from pydantic import BaseModel, EmailStr, validator

# from bcrypt import checkpw
from typing import Optional
import pandas as pd


def fetch_data(cnxn):
    query = "SELECT TOP 10* FROM PATIENTS"
    df = pd.read_sql(query, cnxn)
    return df


# Defining Pydantic models for the request body
class Patient(BaseModel):
    name: str
    location_address: str
    country: str
    tel: str
    email: EmailStr
    referral_no: Optional[str] = None
    access_no: Optional[str] = None
    age: int
    sex: str  # Assuming 'M' or 'F' for male or female
    password: str


class Guardian(BaseModel):
    GuardianName: str
    Relationship: str
    ContactNumber: str
    PatientID: str


class LoginData(BaseModel):
    email: EmailStr
    password: str


class DoctorLoginData(BaseModel):
    Email: EmailStr
    Password: str


class Hospital(BaseModel):
    HospitalName: str
    Address: str
    Country: str
    Type: str
    EmergencyLine: str
    HelpLine: str
    RegNumber: str
    Email: EmailStr
    Telephone: str
    Docs: str
    ContactNumber: str
    # Password: str/


class Doctor(BaseModel):
    DoctorName: str
    Specialty: str
    AccessNumber: str
    LicenseNumber: str
    Status: str  # This will stay as string but will be checked
    Email: EmailStr
    Telephone: str
    Docs: str
    Password: str
    ContactNumber: str

    # Add a validator to check the status value
    @validator("Status")
    def check_status(cls, value):
        if value.lower() not in ["online", "offline"]:
            raise ValueError('Status must be "Online" or "Offline"')
        return value

    # Password: str


class HospitalDoctor(BaseModel):
    HospitalID: int
    DoctorID: int
    # Password: str


class Appointment(BaseModel):
    PatientID: str
    DoctorID: str
    Date: str
    Time: str
    Purpose: str
    Status: str
    Payment_mode: str
    Meeting_type: str
    Notes: str
    # Password: str


class Consultations(BaseModel):
    PatientID: str
    Date: str
    Reason: str
    DoctorID: str
    Status: str
    Notes: str


class Emergency(BaseModel):
    PatientID: str
    HospitalID: str
    Time: str
    Type: str
    Logitude: float
    latitude: float
    Status: str
    Notes: str
    # Password: str


## check if the user exists
def existing_patient(cnxn, email, referral_no):
    query = "SELECT COUNT(1) FROM PATIENTS WHERE Email = ? OR Referral_No = ?;"
    params = (email, referral_no)
    df = pd.read_sql(query, cnxn, params=params)

    if df.iloc[0, 0] > 0:
        return True
    else:
        return False


## store the user in the database
def store_patient(cnxn, new_patient):
    # Assuming new_patient is a Pydantic model, convert it to a dictionary
    new_patient_data = new_patient.dict()

    # Create a cursor object using the connection
    cursor = cnxn.cursor()

    # Construct the SQL query with placeholders for parameters
    placeholders = ", ".join(["?"] * len(new_patient_data))
    columns = ", ".join(new_patient_data.keys())
    sql = f"INSERT INTO PATIENTS ({columns}) VALUES ({placeholders})"

    # Execute the SQL query with the provided parameters
    cursor.execute(sql, list(new_patient_data.values()))

    # Commit the changes to the database
    cnxn.commit()
    # Close the cursor if you are done with it
    cursor.close()

    return True


def store_guardian(cnxn, guardian_data):
    # Convert the Pydantic model to a dictionary if it's not already one
    if not isinstance(guardian_data, dict):
        guardian_data = guardian_data.dict()

    # Create a cursor object using the connection
    cursor = cnxn.cursor()

    # Construct the SQL insert statement with placeholders for parameters
    placeholders = ", ".join(["?"] * len(guardian_data))
    columns = ", ".join(guardian_data.keys())
    sql_insert = f"INSERT INTO Guardians ({columns}) VALUES ({placeholders});"

    # Execute the SQL insert statement with the provided parameters
    cursor.execute(sql_insert, list(guardian_data.values()))

    # Immediately after the insert operation, select the SCOPE_IDENTITY
    cursor.execute("SELECT SCOPE_IDENTITY();")

    # Commiting the changes to the database
    cnxn.commit()

    cursor.close()


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# def patient_login(cnxn,patient_credentials):
#     if not isinstance(patient_credentials, dict):
#         patient_credentials = patient_credentials.dict()
#     cursor = cnxn.cursor()
#     # sql = f"SELECT Name FROM PATIENTS WHERE Email = ? AND Password = ?;"
#     sql = "SELECT Name, Password FROM PATIENTS WHERE Email = ?;"
#     # params = (patient_credentials['email'], patient_credentials['password'])
#     params = (patient_credentials['email'],)
#     cursor.execute(sql, params)
#     result = cursor.fetchone()

#     # Close the cursor
#     cursor.close()
#     # If a result was found and the passwords match
#     if result:
#         # Check if the hashed password matches
#         if checkpw(patient_credentials['password'].decode('utf-8'), result.Password.encode('utf-8')):
#             return {"success": True, "message": "Login successful.", "name": result.Name}
#         else:
#             return {"success": False, "message": "Invalid email or password."}
#     else:
#         return {"success": False, "message": "Invalid email or password."}

#     import pyodbc


def fetch_patient_by_email(cnxn, email):
    cursor = cnxn.cursor()
    # Prepare the SQL query to fetch the patient
    sql = "SELECT Name, Password FROM PATIENTS WHERE Email = ?;"
    cursor.execute(sql, email)
    # Fetch one record, there should only be one patient with this email
    result = cursor.fetchone()
    cursor.close()

    # If a result was found, return it as a dictionary
    if result:
        return {
            "name": result[0],
            "password": result[
                1
            ],  # Assuming that the password is the second column in the SELECT statement
        }
    else:
        return None


def existing_hospital(cnxn, email):
    query = "SELECT COUNT(1) FROM Hospitals WHERE Email = ?;"
    params = (email,)
    df = pd.read_sql(query, cnxn, params=params)

    if df.iloc[0, 0] > 0:
        return True
    else:
        return False


def add_hospital(cnxn, new_hospital):
    new_hospital_data = new_hospital.dict()

    cursor = cnxn.cursor()
    placeholders = ", ".join(["?"] * len(new_hospital_data))
    columns = ", ".join(new_hospital_data.keys())
    sql = f"INSERT INTO Hospitals ({columns}) VALUES ({placeholders})"

    cursor.execute(sql, list(new_hospital_data.values()))
    cnxn.commit()
    cursor.close()
    return True


def existing_doctor(cnxn, email):
    query = "SELECT COUNT(1) FROM Doctors WHERE Email = ?;"
    params = (email,)
    df = pd.read_sql(query, cnxn, params=params)

    if df.iloc[0, 0] > 0:
        return True
    else:
        return False


def add_doctor(cnxn, new_doctor):
    new_doctor_data = new_doctor.dict()

    new_doctor_data["Status"] = new_doctor_data["Status"].lower() == "online"

    cursor = cnxn.cursor()
    placeholders = ", ".join(["?"] * len(new_doctor_data))
    columns = ", ".join(new_doctor_data.keys())
    sql = f"INSERT INTO Doctors ({columns}) VALUES ({placeholders})"

    cursor.execute(sql, list(new_doctor_data.values()))
    cnxn.commit()
    cursor.close()
    return True


def fetch_doctor_by_email(cnxn, email):
    cursor = cnxn.cursor()
    # Prepare the SQL query to fetch the patient
    sql = "SELECT DoctorName, Password FROM Doctors WHERE Email = ?;"
    cursor.execute(sql, email)
    # Fetch one record, there should only be one patient with this email
    result = cursor.fetchone()
    cursor.close()

    # If a result was found, return it as a dictionary
    if result:
        return {
            "DoctorName": result[0],
            "Password": result[
                1
            ],  # Assuming that the password is the second column in the SELECT statement
        }
    else:
        return None


# def doctor_login(cnxn,doctor_credentials):
#     if not isinstance(doctor_credentials, dict):
#         doctor_credentials = doctor_credentials.dict()
#     cursor = cnxn.cursor()
#     # sql = f"SELECT Name FROM PATIENTS WHERE Email = ? AND Password = ?;"
#     sql = "SELECT DoctorName, Password FROM Doctors WHERE Email = ?;"
#     # params = (patient_credentials['email'], patient_credentials['password'])
#     params = (doctor_credentials['Email'],)
#     cursor.execute(sql, params)
#     result = cursor.fetchone()

#     # Close the cursor
#     cursor.close()
#     # If a result was found and the passwords match
#     if result:
#         # Check if the hashed password matches
#         if checkpw(doctor_credentials['password'].decode('utf-8'), result.Password.encode('utf-8')):
#             return {"success": True, "message": "Login successful.", "name": result.DoctorName}
#         else:
#             return {"success": False, "message": "Invalid email or password."}
#     else:
#         return {"success": False, "message": "Invalid email or password."}

# def add_hospital_doctor(cnxn, hospital_doctor: HospitalDoctor):
#     cursor = cnxn.cursor()

#     # Prepare the SQL query to insert the hospital-doctor association
#     sql = "INSERT INTO HospitalDoctors (HospitalID, DoctorID) VALUES (?, ?);"

#     # Execute the query with the values from the hospital_doctor model
#     cursor.execute(sql, (hospital_doctor.HospitalID, hospital_doctor.DoctorID))

#     # Commit the changes to the database
#     cnxn.commit()

#     # Close the cursor
#     cursor.close()

# def add_hospital_doctor_by_regnumber(cnxn, hospital_doctor_by_regnumber: HospitalDoctorByRegNumber):
#     cursor = cnxn.cursor()

#     # First, find the HospitalID using the RegNumber
#     cursor.execute("SELECT HospitalID FROM Hospitals WHERE RegNumber = ?", (hospital_doctor_by_regnumber.RegNumber,))
#     hospital_id_row = cursor.fetchone()
#     if hospital_id_row is None:
#         raise ValueError("No hospital found with the given RegNumber")
#     hospital_id = hospital_id_row[0]

#     # Now, insert the hospital-doctor association using the found HospitalID
#     sql = "INSERT INTO HospitalDoctors (HospitalID, DoctorID) VALUES (?, ?);"
#     cursor.execute(sql, (hospital_id, hospital_doctor_by_regnumber.DoctorID))

#     # Commit the changes to the database
#     cnxn.commit()
#     cursor.close()
