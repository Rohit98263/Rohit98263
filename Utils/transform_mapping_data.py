def extract_expense_data(parsed_data):
    """
    Extracts relevant information from the parsed data and organizes it into a list of dictionaries,
    where each dictionary represents one page, and the keys represent the types of extracted data.

    Parameters:
        parsed_data (list): A list of dictionaries representing parsed data containing information about
                            different expense documents.

    Returns:
        list: A list of dictionaries, where each dictionary represents a page with extracted data.
              The keys in the dictionary are composed of the type and text values found in the summary fields.
    """
    result = []  # List to store dictionaries representing extracted data for each page.

    # Iterate over each document in the parsed data.
    for document in parsed_data:
        # Get expense documents from the current document.
        expense_docs = document.get("ExpenseDocuments", [])

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

            # Append the page dictionary to the result list.
            result.append(page_dict)

    # Return the list containing dictionaries, each representing extracted data for a page.
    return result


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
            
            elif "RECEIVER_BILL_TO" in key:
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