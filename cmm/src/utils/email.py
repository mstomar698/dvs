from s2analytica.settings import CURRENT_ENV



def create_email_msg(ERROR_COACH_NUMBER, CREATE_COACH_NUMBER, DUPLICATE_COACH_NUMBER, current_user, public_url, DEV_MESSAGE, type_of_datainvoked):

    total_rows = len(ERROR_COACH_NUMBER) + len(CREATE_COACH_NUMBER) + len(DUPLICATE_COACH_NUMBER)
    # Get the first 10 items from the list and join them with commas. If the list is longer than 10, add "..." at the end.
    error_value = ', '.join(str(item) for item in ERROR_COACH_NUMBER[:10]) + '...' if len(ERROR_COACH_NUMBER) > 10 else ', '.join(str(item) for item in ERROR_COACH_NUMBER)
    if len(error_value) == 0:
        error_value = "0"
    create_value = ', '.join(str(item) for item in CREATE_COACH_NUMBER[:10]) + '...' if len(CREATE_COACH_NUMBER) > 10 else ', '.join(str(item) for item in CREATE_COACH_NUMBER)
    if len(create_value) == 0:
        create_value = "0"
    update_value = ', '.join(str(item) for item in DUPLICATE_COACH_NUMBER[:10]) + '...' if len(DUPLICATE_COACH_NUMBER) > 10 else ', '.join(str(item) for item in DUPLICATE_COACH_NUMBER)
    if len(update_value) == 0:
        update_value = "0"
    MESSAGE = f"""
Number of rows in the input file is: {total_rows}, out of which:
Number of Issues while loading/updated data: {len(ERROR_COACH_NUMBER)}
Number of Data Loaded: {len(CREATE_COACH_NUMBER)}
Number of Data Updated: {len(DUPLICATE_COACH_NUMBER)}

{type_of_datainvoked} DATA LOAD is invoked by {current_user}

Uploaded File : {public_url}

Issues while loading/updated data: {error_value}

Data Loaded: {create_value}

Duplicate Data: {update_value}

{DEV_MESSAGE}

You have received this email because you were in the mailing list of CMM/s2analytics.
"""
    return MESSAGE


def create_email_files(ERROR_COACH_NUMBER, CREATE_COACH_NUMBER, DUPLICATE_COACH_NUMBER):
    files = []
    # If the length of the list is greater than 10, create a file and store the data in that file.
    if len(ERROR_COACH_NUMBER) > 10:
        file_path = './error_coach_number.txt'
        with open(file_path, 'w') as f:
            f.write(", ".join(str(item) for item in ERROR_COACH_NUMBER))
            f.write("\n")
        files.append(file_path)
    if len(CREATE_COACH_NUMBER) > 10:
            file_path = './create_coach_number.txt'
            with open(file_path, 'w') as f:
                f.write(", ".join(str(item) for item in CREATE_COACH_NUMBER))
                f.write("\n")
            files.append(file_path)
    if len(DUPLICATE_COACH_NUMBER) > 10:
        file_path = './duplicate_coach_number.txt'
        with open(file_path, 'w') as f:
            f.write(", ".join(str(item) for item in DUPLICATE_COACH_NUMBER))
            f.write("\n")
        files.append(file_path)
    return files




def create_email_subject(type_of_datainvoked):
    return f"{type_of_datainvoked} Data Uploaded in CMM {str(CURRENT_ENV).capitalize()}"