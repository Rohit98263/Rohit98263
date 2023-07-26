from openpyxl import load_workbook
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import A2
from services.textractParsing import analyse_document
from io import BytesIO
import os
import boto3
from osicore.db import db
from dateutil import parser
import json
import re
from utils.loggingConfig import *

def serialize(x):
    """
    Serializes a SQLAlchemy database object to a dictionary.

    Parameters:
        - x (SQLAlchemy database object): The object to be serialized.

    Returns:
        A dictionary containing the serialized object attributes.
    """
    ocr_logger.info("Running serialize function")
    return {c.name: str(getattr(x, c.name)) for c in x.__table__.columns} if x is not None else None
   

def convert_excel_to_pdf(file):
    """
    convert excel to pdf
    """
    ocr_logger.info("Running convert excel to pdf function")
    wb = load_workbook(file)
    ws = wb.active
    data = [[cell.value for cell in row] for row in ws.rows]
    buffer = BytesIO() 
    pdf_file = SimpleDocTemplate(buffer, pagesize=A2)
    table = Table(data)
    pdf_file.build([table])
    pdf_data = buffer.getvalue()
    return pdf_data


def key_from_ocr(file):
    """
    get key from ocr invoice
    """
    ocr_logger.info("Running get key from ocr function")
    filename = file.filename
    extension = filename.split(".")[1].lower() if "." in filename else None
    if extension is None:
        ocr_logger.error("File has no extension for get key from ocr function")
        raise ValueError("File has no extension")
    key_value = analyse_document(file.read(), extension)
    lst = []
    for item in key_value.get("data"):  
        lst.append(list(item.keys()))
    ocr_logger.info("Successfully ran get key from ocr function")
    return lst


def get_vault_secret(secret_name):
    """
    Mock function to retrieve secrets from a vault.
    This function returns dummy values for development.
    Replace this function with the actual implementation for production.
    """
    ocr_logger.info("Running mock function to retrieve secrets from vault")
    # Define the secret values for testing
    secrets = {
        "ftp_password": "Srikanth@1214"
    }

    # Check if the secret exists in the mock vault
    if secret_name in secrets:
        vault_key = secrets[secret_name]
        ocr_logger.info("Sucessfuly ran mock function to get secret from vault")
        return vault_key
    else:
        ocr_logger.error("Input secret not found in mock vault")
        raise ValueError(f"Secret '{secret_name}' not found in the mock vault.")


def upload_file_to_s3(file_path, bucket_name, folder_name, CustomerCode):
    """
    This function is used to upload the specimen into the S3 folder.
    """
    ocr_logger.info("Running function to upload file to S3")
    # Create a connection to S3
    s3_client = boto3.client('s3', region_name='us-east-1', aws_access_key_id='AKIA2G47Q5KBUZ3B5C2M',
                             aws_secret_access_key='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')

    # Extract the file name from the file path
    file_name = file_path.split('/')[-1]

    # Specify the S3 key (folder + file name)
    s3_key = f"{folder_name}/{file_name}"

    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        ocr_logger.info("Sucessfully uploaded file to S3")
        return {"Success": {"message": "File uploaded successfully"}}, 200
    except FileNotFoundError:
        ocr_logger.error("Location not found to upload file to S3")
        return {"Error": {"message": "Location not found."}}, 200
    except IOError:
        ocr_logger.error("File could not be uploaded to S3 with IOError")
        return {"Error": {"message": "File could not be uploaded."}}, 400


def read_json_from_s3(bucket_name, osi_json_object):
    """
    This function reads a JSON object from S3.
    """
    ocr_logger.info("Running read json from s3 function")
    # Create a connection to S3
    s3_client = boto3.client('s3',region_name = os.getenv("REGION_NAME"))

    try:
        # Get the JSON object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=osi_json_object)

        # Read the JSON data from the response
        json_data = response['Body'].read().decode('utf-8')

        # Parse the JSON data
        json_object = json.loads(json_data)

        ocr_logger.info("Successfully ran read json from s3 function")
        return json_object
    except FileNotFoundError:
        ocr_logger.error("File not found")
        return {"Error": {"message": "File not found."}}, 200
    except IOError:
        ocr_logger.error("File could not be read")
        return {"Error": {"message": "File could not be read."}}, 400


def create_specimen_folder_by_customer(customer_code, document_type):
    """
    This function creates the folder for uploading the specimen.
    """
    ocr_logger.info("Running function to create folder for uploading the specimen")
    specimen_bucket_name = 'ocr-email/Specimen'

    # Create a connection to S3
    s3_client = boto3.client('s3', region_name='us-east-1', aws_access_key_id='AKIA2G47Q5KBUZ3B5C2M',
                             aws_secret_access_key='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')

    try:
        # Create an empty object with the folder name as the key
        s3_client.put_object(Bucket=specimen_bucket_name, Key=f"{customer_code}/{document_type}")

        ocr_logger.info("Sucessfully ran function to create folder for uploading the specimen")
        print(f"Folder '{customer_code}' created in '{specimen_bucket_name}' successfully.")
        return {"Success": {"message": "Folder created successfully"}}, 200
    except FileNotFoundError:
        ocr_logger.error("File not found")
        return {"Error": {"message": "File not found."}}, 200
    except IOError:
        ocr_logger.error("File could not be read")
        return {"Error": {"message": "File could not be read."}}, 400
    
    
def convert_date_format(date_string, target_format):
    """
    Converts a given date string from one format to another.

    Parameters:
        - date_string (str): The input date string to be converted.
        - target_format (str): The desired format for the output date string.

    Returns:
        The input date string converted to the specified target format,
        or None if the conversion fails.
    """
    try:
        parsed_date = parser.parse(date_string)
        formatted_date = parsed_date.strftime(target_format)
        return formatted_date
    except ValueError:
        return None
    

def sanitize_amount(total_amount):
    """
    Sanitizes a given total amount by removing non-digit and non-decimal characters.

    Parameters:
        - total_amount (str): The total amount to be sanitized.

    Returns:
        The sanitized total amount as a float if it is not None,
        otherwise returns None.
    """
    try:
        if total_amount is not None:
            # total_amount = intotal_amount)
            total_amount = re.sub(r'[^\d.]', '', total_amount)
            total_amount = float(total_amount)
        return total_amount
    except ValueError:
        return None
    

def map_ocr_response(ocr_response, mapping_data):
    """
    Maps the OCR response to a target mapping based on the provided mapping data.

    Parameters:
        - ocr_response (dict): The OCR response containing the data to be mapped.
        - mapping_data (dict): The mapping data defining the target structure.

    Returns:
        - final_mapping (dict): The mapped result based on the provided mapping data.
    """
    final_mapping = {}

    for source_key, source_value in ocr_response.items():
        found_mapping = False

        if source_key == "items":
            # Handle the "items" key separately
            target_list = []
            for item in source_value:
                item_mapping = {}
                for item_key, item_value in item.items():
                    for section in mapping_data["sections"]:
                        mappings = section["mappings"]
                        for mapping in mappings:
                            if mapping["source_key"] == item_key:
                                target_key = mapping["target_key"]
                                item_mapping[target_key] = item_value
                                found_mapping = True
                                break
                if item_mapping:
                    target_list.append(item_mapping)
            final_mapping[source_key] = target_list
        else:
            # Handle other keys
            for section in mapping_data["sections"]:
                mappings = section["mappings"]
                for mapping in mappings:
                    if mapping["source_key"] == source_key:
                        target_key = mapping["target_key"]
                        final_mapping[target_key] = source_value
                        found_mapping = True
                        break

        if not found_mapping:
            continue

    return final_mapping


def add_data_to_database(object):
    db.session.add(object)
    db.session.commit()





