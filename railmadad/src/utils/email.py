from s2analytica.settings import CURRENT_ENV

def create_email_msg(ERROR_REFERENCE_NUMBER, CREATE_REFERENCE_NUMBER, UPDATE_REFERENCE_NUMBER, current_user, public_url, DEV_MESSAGE):

    total_rows = len(ERROR_REFERENCE_NUMBER) + len(CREATE_REFERENCE_NUMBER) + len(UPDATE_REFERENCE_NUMBER)
    # Get the first 10 items from the list and join them with commas. If the list is longer than 10, add "..." at the end.
    error_value = ', '.join(str(item) for item in ERROR_REFERENCE_NUMBER[:10]) + '...' if len(ERROR_REFERENCE_NUMBER) > 10 else ', '.join(str(item) for item in ERROR_REFERENCE_NUMBER)
    if len(error_value) == 0:
        error_value = "0"
    create_value = ', '.join(str(item) for item in CREATE_REFERENCE_NUMBER[:10]) + '...' if len(CREATE_REFERENCE_NUMBER) > 10 else ', '.join(str(item) for item in CREATE_REFERENCE_NUMBER)
    if len(create_value) == 0:
        create_value = "0"
    update_value = ', '.join(str(item) for item in UPDATE_REFERENCE_NUMBER[:10]) + '...' if len(UPDATE_REFERENCE_NUMBER) > 10 else ', '.join(str(item) for item in UPDATE_REFERENCE_NUMBER)
    if len(update_value) == 0:
        update_value = "0"
    MESSAGE = f"""
Number of rows in the input file is: {total_rows}, out of which:
Number of Issues while loading/updated data: {len(ERROR_REFERENCE_NUMBER)}
Number of Data Loaded: {len(CREATE_REFERENCE_NUMBER)}
Number of Data Updated: {len(UPDATE_REFERENCE_NUMBER)}

DATA LOAD is invoked by {current_user}

Uploaded File : {public_url}

Issues while loading/updated data: {error_value}

Data Loaded: {create_value}

Data Updated: {update_value}

{DEV_MESSAGE}

You have received this email because you were in the mailing list of RailMadad.
"""
    return MESSAGE


def create_email_files(ERROR_REFERENCE_NUMBER, CREATE_REFERENCE_NUMBER, UPDATE_REFERENCE_NUMBER):
    files = []
    if len(ERROR_REFERENCE_NUMBER) > 10:
        with open('./error_reference_number.txt', 'w') as f:
            f.write(", ".join(str(item) for item in ERROR_REFERENCE_NUMBER))
            f.write("\n")
        files.append('./error_reference_number.txt')
    if len(CREATE_REFERENCE_NUMBER) > 10:
        with open('./create_reference_number.txt', 'w') as f:
            f.write(", ".join(str(item) for item in CREATE_REFERENCE_NUMBER))
            f.write("\n")
        files.append('./create_reference_number.txt')
    if len(UPDATE_REFERENCE_NUMBER) > 10:
        with open('./update_reference_number.txt', 'w') as f:
            f.write(", ".join(str(item) for item in UPDATE_REFERENCE_NUMBER))
            f.write("\n")
        files.append('./update_reference_number.txt')
    return files


def create_sending_list(current_user):

    prod_mailing_list = ["atul.nitt.cse@gmail.com", "riturajnitt@gmail.com", "mukul0000kumar@gmail.com"]
    local_mailing_list = ["mukul0000kumar@gmail.com"]
    sending_list = []
    if current_user == "alex_test" or CURRENT_ENV == "LOCAL":
        sending_list = local_mailing_list
        sending_list.append(current_user)
    # else :

    print("Sending email to: ", sending_list)
    #     sending_list.append(prod_mailing_list)
    return sending_list

def create_email_subject():
    return f"Data Uploaded in RailMadad {str(CURRENT_ENV).capitalize()}"