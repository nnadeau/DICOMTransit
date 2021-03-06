import logging

from DICOM.validate import DICOM_validator


def DICOM_retrieveElements(file_path, data_element):
    """
    A low level function used to retrieve elements from DICOM and return a LIST of matching element. ACCEPT PARTIAL MATCH
    :param file_path:
    :param data_element:
    :return: LIST of all data elements that match the pattern provided in the data_element and their value.  NO Regular EXPRESSION.
    """
    success, DICOM = DICOM_validator(file_path)
    if not success:
        return False, None, None

    # Get a list of all data elements that can have element label.
    element_values = DICOM.data_element(data_element).value

    return True, element_values


def DICOM_updateElement(file_path, data_element, element_value, out_path):
    """
    Update a particular data_element to the desired value, then write back to the SOURCE FILE!
    :param file_path:
    :param data_element:
    :param element_value:
    :return: bool on operation success, and string on reason.
    """

    """BE AWARE that if the key does not exist, it will not be created currently!"""
    logger = logging.getLogger(__name__)
    success, DICOM = DICOM_validator(file_path)
    if not success:
        return False, "DICOM not valid."

    try:
        DICOM.data_element(data_element).value = element_value
    except KeyError:
        logger.info("Key " + data_element + " does not exist, creating the key.")
        return False, "DICOM key field does not exist. Not sure how to create one yet. "
    DICOM.save_as(out_path)
    return True, "Data element update completed."


def DICOM_retrieveMRN(file_path):
    """
    Read the PatientID field which normally used as MRN number.
    :param file_path:
    :return: MRN number, as a STRING
    """
    success, value = DICOM_retrieveElements(file_path, "PatientID")

    if not success:
        return False, None
    else:
        return True, value


def DICOM_computeScanAge(file_path):
    """
    Read the PatientID field which normally used as MRN number.
    :param file_path:
    :return: Age as a relative delta time object.
    """

    from dateutil.relativedelta import relativedelta

    success, DICOM = DICOM_validator(file_path)
    if not success:
        return False, None
    from datetime import datetime
    scan_date = datetime.strptime(DICOM.SeriesDate, "%Y%m%d")
    birthday = datetime.strptime(DICOM.PatientBirthDate, "%Y%m%d")
    age = relativedelta(scan_date, birthday)
    return True, age