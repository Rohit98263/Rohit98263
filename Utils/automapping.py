import boto3
import json
import time


def read_json_from_s3(bucket_name, osi_json_object):
    """
    This function reads a JSON object from S3.
    """
    # ocr_logger.info("Running read json from s3 function")
    # Create a connection to S3
    s3_client = boto3.client('s3')

    try:
        # Get the JSON object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=osi_json_object)

        # Read the JSON data from the response
        json_data = response['Body'].read().decode('utf-8')

        # Parse the JSON data
        json_object = json.loads(json_data)

        # ocr_logger.info("Successfully ran read json from s3 function")
        return json_object
    except FileNotFoundError:
        # ocr_logger.error("File not found")
        return {"Error": {"message": "File not found."}}, 200
    except IOError:
        # ocr_logger.error("File could not be read")
        return {"Error": {"message": "File could not be read."}}, 400


def update_source_keys(mapping_data, source_data):
    """
    Updates the source_key in the mapping_data based on the selectedValue from the source_data.

    Args:
        mapping_data (dict): Mapping object model containing sections and mappings.
        source_data (dict): Source data containing source keys and selected values.

    Returns:
        dict: Updated mapping_data with modified source_key values.

    """
    for source_item in source_data["sourceData"]:
        selected_value = source_item.get("selectedValue")  # Use get() to safely get the value or return None
        source_key = source_item.get("sourcekey")  # Use get() to safely get the value or return None
        if selected_value and source_key:  # Check if both selected_value and source_key exist
            for section in mapping_data["sections"]:
                mappings = section["mappings"]
                for mapping in mappings:
                    if mapping["source_display_name"] == selected_value:
                        mapping["source_key"] = source_key
                        break
        
    # Check if ItemData is present
    if "ItemsData" in source_data:
        items_data = source_data["ItemsData"]
        for item in items_data:
            selected_value = item.get("selectedValue")  # Use get() to safely get the value or return None
            source_key = item.get("sourcekey")  # Use get() to safely get the value or return None
            if selected_value and source_key:  # Check if both selected_value and source_key exist
                for section in mapping_data["sections"]:
                    mappings = section["mappings"]
                    for mapping in mappings:
                        if mapping["source_display_name"] == selected_value:
                            mapping["source_key"] = source_key
                            break

    return mapping_data


def start_expense_analysis(bucket_name, document_key):
    """
    Start the asynchronous expense analysis for the PDF document.

    Parameters:
        bucket_name (str): The name of the S3 bucket containing the PDF document.
        document_key (str): The object key of the PDF document in the S3 bucket.

    Returns:
        str: The JobId of the started Textract job.
    """
    textract_client = boto3.client('textract')
    response = textract_client.start_expense_analysis(
        DocumentLocation={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': document_key
            }
        }
    )
    return response['JobId']

def get_expense_analysis_result(job_id):
    """
    Check the job status and retrieve the results of the expense analysis.

    Parameters:
        job_id (str): The JobId of the Textract job.

    Returns:
        list: A list of dictionaries, where each dictionary represents a page with extracted data.
              The keys in the dictionary are composed of the type and text values found in the summary fields.
    """
    textract_client = boto3.client('textract')

    while True:
        response = textract_client.get_expense_analysis(JobId=job_id)
        status = response['JobStatus']

        if status in ['SUCCEEDED', 'FAILED']:
            break  # Processing is complete or failed, exit the loop

        # Wait for a few seconds before checking the status again
        

    if status == 'SUCCEEDED':
        new_dict = {}
        
        if len(response['ExpenseDocuments']) > 0:
            result = extract_expense_data(response)
            new_dict["data"] = result
            return new_dict
    else:
        print("Expense analysis failed. Error message:", response['StatusMessage'])
        return []

def extract_expense_data(parsed_data):
    """
    Extracts relevant information from the parsed data and organizes it into a list of dictionaries,
    where each dictionary represents one page, and the keys represent the types of extracted data.

    Parameters:
        parsed_data (dict): The parsed data containing information about different expense documents.

    Returns:
        list: A list of dictionaries, where each dictionary represents a page with extracted data.
              The keys in the dictionary are composed of the type and text values found in the summary fields.
    """
    result = []  # List to store dictionaries representing extracted data for each page.

    # Get expense documents from the parsed data.
    expense_docs = parsed_data.get("ExpenseDocuments", [])

    # Iterate over each expense document.
    for expense_doc in expense_docs:
        # Get the page number from the first summary field of the current expense document (if available).
        page_number = expense_doc.get("SummaryFields", [])[0].get("PageNumber")

        # Create an empty dictionary to store the extracted data for the current page.
        page_dict = {}

        # Iterate over each summary field in the current expense document.
        for summary_field in expense_doc.get("SummaryFields", []):
            # Get the "Type" text and "ValueDetection" text from the current summary field.
            type_text = summary_field.get("Type", {}).get("Text", "")
            text_value = summary_field.get("ValueDetection", {}).get("Text", "")

            # Check if the "GroupProperties" exist in the current summary field.
            if "GroupProperties" in summary_field:
                group_properties = summary_field["GroupProperties"]
                for group_prop in group_properties:
                    types = group_prop.get("Types", [])
                    # Concatenate type and text value to form a key and store the text value as its corresponding value.
                    if types:
                        for type_val in types:
                            key = f"{type_val}.{type_text}"
                            value = text_value
                            page_dict[key] = value
            else:
                # Add type_text and text_value as a key-value pair in the page_dict.
                page_dict[type_text] = text_value

        line_item_groups = expense_doc.get("LineItemGroups", [])
        if line_item_groups:
            line_items = []
            for group in line_item_groups:
                for line_item in group.get("LineItems", []):
                    line_item_data = {}
                    for expense_field in line_item.get("LineItemExpenseFields", []):
                        key = expense_field.get("Type", {}).get("Text", "")
                        value = expense_field.get("ValueDetection", {}).get("Text", "")
                        line_item_data[key] = value
                    line_items.append(line_item_data)
            page_dict["items"] = line_items

        # Append the page dictionary to the result list.
        result.append(page_dict)
    return result

# Example usage:

# if job_id:
#     result = get_expense_analysis_result(job_id)
#     print(result)

import json

def create_payload(result):
    """
    Converts the provided 'result' list into a 'payload' JSON string with mapped objects based on specific conditions.

    Parameters:
        result (list): A list of dictionaries, where each dictionary represents extracted data for a page.
                       The keys in the dictionary are composed of the type and text values found in the summary fields.

    Returns:
        str: A JSON string representing the 'payload' containing mapped objects based on the provided conditions.
    """
    mapped_objects_list = []
    mapped_objects_dict = {}
    for item in result["data"]:
         # Create a new dictionary for each item in the result

        for key, value in item.items():
            mapped_objects = {} 
            if "VENDOR" in key:
                if ".CITY" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Buyer City"
                elif ".ADDRESS" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Buyer Address"
                elif ".STREET" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Buyer Street"
                elif ".STATE" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Buyer State"
                elif ".NAME" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Buyer Name"
                elif ".ZIP_CODE" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Buyer Zip Code"
            elif "RECEIVER_SOLD_TO" in key:
                if ".ADDRESS" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Seller Address"
                elif ".STREET" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Seller Street"
                elif ".CITY" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Seller City"
                elif ".STATE" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Seller State"
                elif ".ZIP_CODE" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Seller Zip Code"
                elif ".NAME" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Seller Name"
                elif ".ADDRESS_BLOCK" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Seller Address"
            elif "RECEIVER_SHIP_TO" in key:
                if ".ADDRESS" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Ship to Address Line 1"
                elif ".STREET" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "null"
                elif ".CITY" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Ship to Location"
                elif ".STATE" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "null"
                elif ".ZIP_CODE" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Ship to PIN"
                elif ".NAME" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Ship to Legal Name"
                elif ".ADDRESS_BLOCK" in key:
                    mapped_objects["sourcekey"] = key
                    mapped_objects["selectedValue"] = "Ship to Address Line 1"
            
            elif "INVOICE_RECEIPT_ID" in key:
                mapped_objects["sourcekey"] = key
                mapped_objects["selectedValue"] = "Invoice Number"
            
            elif "INVOICE_RECEIPT_DATE" in key:
                mapped_objects["sourcekey"] = key
                mapped_objects["selectedValue"] = "Invoice Date"
                
            elif "AMOUNT_DUE" in key:
                mapped_objects["sourcekey"] = key
                mapped_objects["selectedValue"] = "Payment Due"
        
            elif "TOTAL" in key:
                mapped_objects["sourcekey"] = key
                mapped_objects["selectedValue"] = "Invoice Total Value"
        # Append the mapped_objects dictionary to the list
            mapped_objects_list.append(mapped_objects)
            
    # Convert the list of mapped_objects to a JSON string and return it
    # payload = json.dumps(mapped_objects_list)
    mapped_objects_dict["sourceData"] = mapped_objects_list
    return mapped_objects_dict



bucket_name = 'aiscan-web-process-document'
document_key = 'INVOICE@CAC-INC.pdf'

job_id = start_expense_analysis(bucket_name, document_key)
async_result = get_expense_analysis_result(job_id)

payload = create_payload(async_result)
# print(payload)


bucket_name = "osi-object-mapping-model"
osi_json_file = "Static/MappingObjectV6.json"

# Retrieve the OSI JSON object from S3
osi_json_object = read_json_from_s3(bucket_name, osi_json_file)


result = update_source_keys(osi_json_object,payload)
print(result)