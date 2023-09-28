import copy
import os

import logging
import threading
import pytz
import warnings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime as dt
from railmadad.constants import update_global_variables
from railmadad.models import CsvFile, Main_Data_Upload
from dateutil.parser import parse as date_parse
import pandas as pd
from railmadad.src.utils.email import create_email_msg, create_email_files,  create_email_subject
from s2analytica.common import log_time, getratelimit

from s2analytica.utils.email import SendEmail
from s2analytica.settings import CMM__DRIVE_FOLDER_ID, RAILMADAD__DRIVE_FOLDER_ID, SERVICE_ACCOUNT_FILE
from s2analytica.settings import EMAIL_HOST_USER
from s2analytica.utils.save import save_file_to_disk, upload_file_to_drive

from s2analytica.utils.email import create_sending_list
from django_ratelimit.decorators import ratelimit

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

# current_env = os.getenv("ENV")

IST = pytz.timezone('Asia/Kolkata')

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
@csrf_exempt
def upload_data(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        if user.groups.filter(name="Moderator").exists():
            now = dt.now(IST)
            csv_data = request.FILES.get("csv")
            td = DataUpload(csv_data, user, now, request)
            td.start()
            messages.success(request, "Your data is Uploaded and is being processed. You will recieve an email once it is done.")
            return redirect(request.path)
        else:
            return redirect(request.path)
    return render(request, "railmadad/data_upload.html")





class DataUpload(threading.Thread):
    def __init__(self, csv_data, user, time, request):
        self.csv_data = copy.deepcopy(csv_data)
        self.user = user
        now = dt.now(IST)
        dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
        ENV = os.getenv("ENV")
        self.drive_file_name = f'{ENV}-{user}-{dt_string}-{csv_data.name}'
        self.local_file_name = csv_data.name
        self.now = time
        self.request = request
        threading.Thread.__init__(self)

    def run(self):
        # save here
        save_file_to_disk(self.local_file_name, self.csv_data)
        print("File saved to disk")
        public_url = ""
        try:
            public_url = upload_file_to_drive(self.drive_file_name, self.local_file_name, SERVICE_ACCOUNT_FILE, RAILMADAD__DRIVE_FOLDER_ID)
            # save a reference of the url in the database
            csvfileurl = CsvFile.objects.create(csv_drive_url_path=public_url)
            csvfileurl.save()
        except:
            pass
        self.df = pd.read_csv( self.local_file_name , encoding = "ISO-8859-1") # adding encoding type to include special character in comments.
        os.remove(self.local_file_name)
        # fill na with -1
        self.df = self.df.fillna(-1)
        print("File removed from disk")
        CREATE_REFERENCE_NUMBER = []
        UPDATE_REFERENCE_NUMBER = []
        ERROR_REFERENCE_NUMBER = []
        empty_reference_number_count = 0
        reference_number = -1
        developers_msg = ""
        try:
            length = len(self.df)
            for i in range(0, length):
                try:
                    try:
                        sl_number = (self.df["S. No."][i])
                    except KeyError as e:
                        sl_number = "-1"
                    try:
                        reference_number = int(self.df["Ref. No."][i])
                        if reference_number == -1:
                            raise ValueError("You have provided an empty reference nuumber in the csv file. Open the csv in text editor.")
                    except KeyError as e:
                        raise ValueError("Issue while reading reference_number")
                        # raise ValueError("Issue while reading reference_number")
                    if (
                        self.df["Registration Date"][i] == " "
                        or type(self.df["Registration Date"][i]) == float
                    ):
                        raise ValueError("Issue while reading registeration_date")
                        # raise ValueError("Issue while reading registeration_date")
                    else:
                        registeration_date = date_parse(
                            self.df["Registration Date"][i], dayfirst=True)
                    if self.df["Closing Date"][i] == " " or type(self.df["Closing Date"][i]) == float:
                        closing_date = dt.strptime(
                            f"01-01-99 00:00", "%m/%d/%y:00-00"
                        )
                    else:
                        closing_date = date_parse(self.df["Closing Date"][i], dayfirst=True)
                    if self.df["Disposal Time"][i] == "nan" or self.df["Disposal Time"][i] == "" or self.df["Disposal Time"][i] == " " or self.df["Disposal Time"][i] == None or self.df["Disposal Time"][i] == 'None' or self.df["Disposal Time"][i] == "nan":
                        disposal_time = float(0)
                    else:
                        disposal_time_str = str(self.df["Disposal Time"][i])
                        disposal_time_str = disposal_time_str.replace(";", ":")
                        disposal_time = disposal_time_str.replace(":", ".")
                        if len(disposal_time.split(".")) > 2:
                            disposal_time = float(str(disposal_time.split(
                                ".")[0] + "." + disposal_time.split(".")[1]))
                    try:
                        train_coach_type = (self.df["Train Coach Type"][i])
                    except KeyError as e:
                        train_coach_type = "-1"
                    try:
                        physical_coach_number = float(
                            self.df["Coach No."][i])
                    except Exception as e:
                        physical_coach_number = -1
                    try:
                        physical_coach_type = self.df["Coach Type"][i]
                    except KeyError as e:
                        physical_coach_type = "-1"
                    try:
                        rake_number = int(self.df["Rake No."][i])
                    except :
                        rake_number = "-1"
                    try:
                        problem_type = (self.df["Type"][i])
                        if problem_type == "Corruption / Bribery":
                            problem_type = "Corruption Bribery"
                            # main_data.save()
                        elif problem_type == "Catering & Vending Services":
                            problem_type = "Catering and Vending Services"
                    except KeyError as e:
                        problem_type = "-1"
                    try:
                        sub_problem_type = (self.df["Sub Type"][i])
                    except KeyError as e:
                        sub_problem_type = "-1"
                    try:
                        staff_name = (self.df["Escot staff"][i])
                    except KeyError as e:
                        try:
                            staff_name = (self.df["Escorting Staff"][i])
                        except KeyError as e:
                            staff_name = "-1"
                    try:
                        dept = (self.df["Dept"][i])
                    except KeyError as e:
                        dept = "-1"

                    try:
                        rating = self.df["Rating"][i]
                        # print(rating)
                        if rating == "nan" or rating == None or rating == "" or rating == " " or rating == "None" or rating == "NaN" or rating == "nan" or rating == "Nan" or rating == "NAN" or rating == "None":
                            rating = "-1"
                    except:
                        rating = "-1"
                    # print("rating", rating)
                    try:
                        train_coach_number = int(self.df["Train Coach No."][i])
                    except :
                        train_coach_number = "-1"
                    try:
                        upcoming_station = (self.df["Upcoming Station"][i])
                    except KeyError as e:
                        upcoming_station = "-1"
                    try:
                        mob_email_id = (self.df["Mobile No./Email Id"][i])
                    except KeyError as e:
                        mob_email_id = "-1"
                    try:
                        train_name = (self.df["Train Name"][i])
                    except KeyError as e:
                        train_name = "-1"
                    try:
                        current_user_id = (self.df["Current User Id"][i])
                    except KeyError as e:
                        current_user_id = "-1"
                    try:
                        current_user_mobile_number = (
                            self.df["Current User Mobile No"][i])
                    except KeyError as e:
                        current_user_mobile_number = "-1"
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        obj, created = Main_Data_Upload.objects.update_or_create(
                            reference_number=reference_number,
                            defaults={
                                "sl_number": sl_number,
                                "reference_number": reference_number,
                                "registration_date": registeration_date,
                                "closing_date": closing_date,
                                "disposal_time": disposal_time,
                                "train_station": self.df["Train/Station"][i],
                                "train_coach_type": train_coach_type,
                                "physical_coach_number": physical_coach_number,
                                "rake_number": rake_number,
                                "staff_name": staff_name,
                                "problem_type": problem_type,
                                "sub_type": sub_problem_type,
                                "zone": self.df["Zone"][i],
                                "div": self.df["Div"][i],
                                "dept": dept,
                                "breach": self.df["Breach"][i],
                                "rating": rating,
                                "status": self.df["Status"][i],
                                "complaint_discription": self.df["Complaint Description"][i],
                                "remark": self.df["Remarks"][i],
                                "number_of_time_forwarded": self.df["No. of times forwarded"][i],
                                "pnr_utc_number": self.df["PNR/UTS No"][i],
                                "physical_coach_type": physical_coach_type,
                                "train_coach_number": train_coach_number,
                                "feedback_remark": self.df["Feedback Remarks"][i],
                                "upcoming_station": upcoming_station,
                                "mobile_number_or_email": mob_email_id,
                                "train_name": train_name,
                                "current_user_id": current_user_id,
                                "current_user_mobile_number": current_user_mobile_number,
                                "updated_at": self.now,
                                "updated_by": str(self.request.user.username),
                            }
                        )
                        obj.save()
                        if created is True:
                            CREATE_REFERENCE_NUMBER.append(reference_number)
                            ob, created = Main_Data_Upload.objects.update_or_create(
                                reference_number=reference_number,
                                defaults={
                                    "sl_number": sl_number,
                                    "reference_number": reference_number,
                                    "registration_date": registeration_date,
                                    "closing_date": closing_date,
                                    "disposal_time": disposal_time,
                                    "train_station": self.df["Train/Station"][i],
                                    "train_coach_type": train_coach_type,
                                    "physical_coach_number": physical_coach_number,
                                    "rake_number": rake_number,
                                    "staff_name": staff_name,
                                    "problem_type": problem_type,
                                    "sub_type": sub_problem_type,
                                    "zone": self.df["Zone"][i],
                                    "div": self.df["Div"][i],
                                    # "owning_zone": owning_zone,
                                    # "owning_div": owning_div,
                                    "dept": dept,
                                    "breach": self.df["Breach"][i],
                                    "rating": self.df["Rating"][i],
                                    "status": self.df["Status"][i],
                                    "complaint_discription": self.df["Complaint Description"][i],
                                    "remark": self.df["Remarks"][i],
                                    "number_of_time_forwarded": self.df["No. of times forwarded"][i],
                                    "pnr_utc_number": self.df["PNR/UTS No"][i],
                                    "physical_coach_type": physical_coach_type,
                                    "train_coach_number": train_coach_number,
                                    "feedback_remark": self.df["Feedback Remarks"][i],
                                    "upcoming_station": upcoming_station,
                                    "mobile_number_or_email": mob_email_id,
                                    "train_name": train_name,
                                    "current_user_id": current_user_id,
                                    "current_user_mobile_number": current_user_mobile_number,
                                    "updated_at": self.now,
                                    "updated_by": str(self.request.user.username),
                                    "created_at": self.now,
                                    "created_by": self.user,
                                }
                            )
                            ob.save()
                        else:
                            UPDATE_REFERENCE_NUMBER.append(reference_number)
                except Exception as ex:
                    # append ex in developers message
                    if ex == "You have provided an empty reference nuumber in the csv file. Open the csv in text editor." or reference_number == -1:
                        empty_reference_number_count += 1
                    else:
                        developers_msg = f"{developers_msg}\n{reference_number}: {ex}"
                        ERROR_REFERENCE_NUMBER.append(reference_number)

                    logging.error(f"{reference_number} - {ex}")
                    pass
            if empty_reference_number_count > 0:
                developers_msg = f"{developers_msg}\n{empty_reference_number_count} empty reference number found in the csv file. Open the csv in text editor."

        except Exception as e:
            print(e)

            msg_info = f'Please re-check the data Column And Upload Again. Problem with the reference number {ERROR_REFERENCE_NUMBER}'
        
        # if len(ERROR_REFERENCE_NUMBER) > 0:

        update_global_variables()

        email_msg = create_email_msg(
            ERROR_REFERENCE_NUMBER=ERROR_REFERENCE_NUMBER, 
            CREATE_REFERENCE_NUMBER=CREATE_REFERENCE_NUMBER, 
            UPDATE_REFERENCE_NUMBER=UPDATE_REFERENCE_NUMBER,
            current_user=self.request.user.username,
            DEV_MESSAGE=developers_msg,
            public_url=public_url
            )
        
        email_sub = create_email_subject()

        email_list = create_sending_list(self.request.user.email)

        email_files = create_email_files(
            CREATE_REFERENCE_NUMBER=CREATE_REFERENCE_NUMBER, 
            UPDATE_REFERENCE_NUMBER=UPDATE_REFERENCE_NUMBER, 
            ERROR_REFERENCE_NUMBER=ERROR_REFERENCE_NUMBER
            )
        
        SendEmail(email_sub, email_msg, EMAIL_HOST_USER, email_list, email_files)

        # Cleanup temproary files
        for file_path in email_files:
            os.remove(file_path)
        



