def search_document_type(text):
    """
    Searches for the document type in the text

    Parameters:
        text (string): text extracted from the image

    Returns:
        list: list of indices of the document type occurences
    """
    # initializing the list of document types
    key_indices = []

    # searching for document type in the text
    # suggested update :- use regex to search for the document type
    key_indices.append(text.find('invoice'))
    key_indices.append(text.find('purchaseorder'))
    key_indices.append(text.find('salesorder'))

    # returning indices of the document type occurences
    return key_indices


def extract_text(img):
    """
    Extracts the text from the image

    Parameters:
        img (numpy.ndarray): image

    Returns:
        string: extracted text
    """
    # extracting the text from the image and converting it to lowercase
    text = pytesseract.image_to_string(img)
    text = text.lower()
    return text


def identify_document_type(document, file_path):
    """
    Identifies the type of the document
    
    Parameters:
        document (byte): document to be identified
    
    Returns:
        string: type of the document
        invalid: if the document type is invalid
    """
    #document_type = None
    image_extensions = ['jpg','png','jpeg','webp','tiff','bmp']
    if document != None:
        extension = file_path.split('.')[-1].lower()
        if extension == 'pdf':
            document_type = 'pdf'

            # converting the pdf to bytes
            document = document.read()
            # converting the bytes to image
            pages = convert_from_bytes(document)
            page = pages[0]
        elif extension in image_extensions:
            document_type = 'image'
            page = Image.open(document)
        else:
            document_type = 'invalid'
    return document_type, np.array(page)


def find_min_positive_index(list):
    """
    Returns the index of the minimum positive value in the list

    Parameters:
        list (list): list of integers

    Returns:
        int: index of the minimum positive value in the list
        -1: if no positive value is found
    """
    min = sys.maxsize
    # min_index = -1
    min_index = 0
    for i in range(len(list)):
        if list[i] < min and list[i] >= 0:
            min = list[i]
            min_index = i
    return min_index


def check_quality(text):
    """
    Checks the quality of the image

    Parameters:
        text (string): text extracted from the image

    Returns:
        bool: False if the quality of the image is low 
    """
    if len(text) > 40:
        return True
    return False


def classify_document(file_path):
    """
    Extracts the text from the document and classifies it into one of the following categories:
    1. Invoice
    2. Purchase Order
    3. Sales Order

    Parameters:
        file_path: bucket location of the document

    Returns:
        prints {"file_type": "invoice"/"purchase order"/"sales order"}
    """
    s3_client = boto3.client('s3')
    try:
        obj = s3_client.get_object(Bucket = os.getenv("ONESCAN_BUCKET"), Key = file_path)
    except s3_client.exceptions.NoSuchKey:
        raise Exception(f'File {file_path} does not exist in the S3 bucket.')
    except Exception as e:
        raise Exception(f'Failed to retrieve file from S3: {str(e)}')
    document = obj['Body']
    # check document type and store the image
    document_type, page = identify_document_type(document, file_path)

    # return error if document type is invalid
    if document_type == 'invalid':
        if len(list(document.read())) == 0:
            return {"Error": "No file selected"}
        return {"Error": "Invalid document"}

    # cropping the image to the top 1/2th
    img = page
    height, width = img.shape[:2]
    img = img[:height//2, :]

    # extracting the text from the image and converting it to lowercase
    text = extract_text(img)

    #removing all whitespaces from the text
    text = ''.join(text.split())

    keys = ['Invoice', 'PO', 'SO']

    # searching for the document type in the text
    key_indices = search_document_type(text)

    # returning the document type
    min_index = find_min_positive_index(key_indices)
    if min_index == -1:
        if(check_quality(text)):
            return {"file_type": "supporting document", "document_type": document_type}
        return {"Error": "Invalid Document or Low Quality Image. Please reupload."}

    return keys[min_index]


def webrequest_classify_document(file_path):
    """
    Extracts the text from the document and classifies it into one of the following categories:
    1. Invoice
    2. Purchase Order
    3. Sales Order

    Parameters:
        file_path: bucket location of the document

    Returns:
        prints {"file_type": "invoice"/"purchase order"/"sales order"}
    """
    ocr_logger.info("Running classify document function")
    s3_client = boto3.client('s3')
    try:
        obj = s3_client.get_object(Bucket = os.getenv("ONESCAN_BUCKET"), Key = file_path)
    except s3_client.exceptions.NoSuchKey:
        ocr_logger.error(f'File {file_path} does not exist in the S3 bucket.')
        raise Exception(f'File {file_path} does not exist in the S3 bucket.')
    except Exception as e:
        ocr_logger.error(f'Failed to retrieve file from S3: {str(e)}')
        raise Exception(f'Failed to retrieve file from S3: {str(e)}')
    document = obj['Body']
    # check document type and store the image
    document_type, page = identify_document_type(document, file_path)

    # return error if document type is invalid
    if document_type == 'invalid':
        if len(list(document.read())) == 0:
            ocr_logger.error(ErrorCodes.NO_FILE_SELECTED["Error"]["message"])
            return ErrorCodes.NO_FILE_SELECTED["Error"], ErrorCodes.NO_FILE_SELECTED["status_code"]
        ocr_logger.error(ErrorCodes.INVALID_DOCUMENT["Error"]["message"])
        return ErrorCodes.INVALID_DOCUMENT["Error"],ErrorCodes.INVALID_DOCUMENT["status_code"]

    # cropping the image to the top 1/2th
    img = page
    height, width = img.shape[:2]
    img = img[:height//2, :]

    # extracting the text from the image and converting it to lowercase
    text = extract_text(img)

    #removing all whitespaces from the text
    text = ''.join(text.split())

    keys = ['Invoice', 'PO', 'SO']

    # searching for the document type in the text
    key_indices = search_document_type(text)

    # returning the document type
    min_index = find_min_positive_index(key_indices)
    if min_index == -1:
        if(check_quality(text)):
            return {"file_type": "supporting document", "document_type": document_type}
        ocr_logger.error(ErrorCodes.LOW_QUALITY["Error"]["message"])
        return ErrorCodes.LOW_QUALITY["Error"],ErrorCodes.LOW_QUALITY["status_code"]

    return keys[min_index]


def document_type_identification(document):
    """
    Identifies the type of the document
    
    Parameters:
        document (byte): document to be identified
    
    Returns:
        string: type of the document
        invalid: if the document type is invalid
    """
    #document_type = None
    image_extensions = ['jpg','png','jpeg','webp','tiff','bmp']
    if document != None:
        extension = document.filename.split('.')[-1].lower()
        if extension == 'pdf':
            document_type = 'pdf'

            # converting the pdf to bytes
            document = document.read()
            # converting the bytes to image
            pages = convert_from_bytes(document)
            page = pages[0]
        elif extension in image_extensions:
            document_type = 'image'
            page = Image.open(document)
        else:
            document_type = 'invalid'

    return document_type, np.array(page)


def document_classification(file):
    """
    Extracts the text from the document and classifies it into one of the following categories:
    1. Invoice
    2. Purchase Order
    3. Sales Order

    Parameters:
        File(File Storage Object) : File accessed from postman

    Returns:
        json: {"file_type": "invoice"/"purchase order"/"sales order"}
    """
    # reading file from request
    document = file
    #document = request.files.get('document')
    
    # check document type and store the image
    document_type, page = document_type_identification(document)

    # return error if document type is invalid
    if document_type == 'invalid':
        if len(list(document.read())) == 0:
            ocr_logger.error(ErrorCodes.NO_FILE_SELECTED["Error"]["message"])
            return ErrorCodes.NO_FILE_SELECTED["Error"], ErrorCodes.NO_FILE_SELECTED["status_code"]
        ocr_logger.error(ErrorCodes.INVALID_DOCUMENT["Error"]["message"])
        return ErrorCodes.INVALID_DOCUMENT["Error"],ErrorCodes.INVALID_DOCUMENT["status_code"]

    # cropping the image to the top 1/2th
    img = page
    height, width = img.shape[:2]
    img = img[:height//2, :]

    # extracting the text from the image and converting it to lowercase
    text = extract_text(img)

    #removing all whitespaces from the text
    text = ''.join(text.split())

    keys = ['Invoice', 'PO', 'SO']

    # searching for the document type in the text
    key_indices = search_document_type(text)

    # returning the document type
    min_index = find_min_positive_index(key_indices)
    if min_index == -1:
        if(check_quality(text)):
            return {"file_type": "supporting document", "document_type": document_type}, 200
        ocr_logger.error(ErrorCodes.LOW_QUALITY["Error"]["message"])
        return ErrorCodes.LOW_QUALITY["Error"],ErrorCodes.LOW_QUALITY["status_code"]
    
    return keys[min_index]
