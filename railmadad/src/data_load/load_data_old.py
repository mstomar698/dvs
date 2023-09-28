from s2analytica.common import log_time, getratelimit
from s2analytica.settings import IST
from django.shortcuts import render
from railmadad.models import Main_Data_Upload, CsvFile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime as dt
from dateutil import parser as date_parse
from django_ratelimit.decorators import ratelimit

@log_time
@ratelimit(key='ip', rate=getratelimit)
@login_required # type: ignore
@csrf_exempt
def old_upload_data(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        ERROR_REFERENCE_NUMBER = []
        if user.groups.filter(name="Moderator").exists():
            now = dt.now(IST)
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            csv_data = request.FILES.get("csv")

            # timestamp = str(int(time.time()))
            convert_data = str(csv_data).split(" ")
            # print(convert_data)
            main_csv_data = "_".join(convert_data)
            # print(main_csv_data)

            # data = CsvFile(csv_data=csv_data)
            # data.save()
            # print(data.get_path())
            try:
                df = pd.read_csv(
                    csv_data)
                # df = pd.read_csv(csv_data)


# In future this will be on a new thread and will be done in background and we will be storing it in s3 rather than on local storage.

                length = len(df)
                # S.NO	Ref. No.	Registration Date	Closing Date	Disposal Time	Train/Station	COACH TYPE	COACH NO
                # RAKE NO	ESCORTING STAff	Type	Sub Type	Div	Owning Zone	Owning Div	Dept	Rating	Status	Complaint Description
                # Remarks	No. of times forwarded	PNR/UTS No	Coach Type	Coach No.	Feedback Remarks	Upcoming Station	Mobile No./Email Id	Physical Coach No
                # Train Name	Current User Id	Current User Mobile No
            except:
                messages.error(
                    request,
                    'Uploaded should be only in Csv format and name of file should only contain space ex:- "file 1.csv","this file.csv" not any special characters including "-","_","!"--->this should not be name of file ex:-this(file).csv',
                )
                return redirect(request.path)
            try:
                for i in range(0, length):
                    try:
                        try:
                            sl_number = (df["Sl. No."][i])
                        except KeyError as e:
                            sl_number = "-1"

                        try:
                            reference_number = int(df["Ref. No."][i])
                        except KeyError as e:
                            messages.error(
                                request, 'Please re-check the data for reference_number')
                            # raise ValueError("Issue while reading reference_number")
                            return redirect(request.path)

                        if (
                            df["Registration Date"][i] == " "
                            or type(df["Registration Date"][i]) == float
                        ):
                            messages.error(
                                request, 'Please re-check the data for registeration_date')
                            # raise ValueError("Issue while reading registeration_date")
                            return redirect(request.path)
                        else:
                            split_date = df["Registration Date"][i].split(" ")
                            register_datee = dt.strptime(
                                f"{split_date[0]}", "%d-%m-%y").strftime("%Y-%m-%d")
                            register_time = f"{split_date[1]}"
                            registeration_date = date_parse(
                                f"{register_datee} {register_time}:00-00"
                            )

                        if df["Closing Date"][i] == " " or type(df["Closing Date"][i]) == float:
                            closing_date = dt.strptime(
                                f"01-01-99 00:00", "%d-%m-%y:00-00"
                            )
                        else:
                            split_date_2 = df["Closing Date"][i].split(" ")
                            closing_datee = dt.strptime(
                                f"{split_date_2[0]}", "%d-%m-%y"
                            )
                            closing_time = f"{split_date_2[1]}"
                            closing_date = date_parse(
                                f"{closing_datee} {closing_time}:00-00"
                            )

                        if df["Disposal Time"][i] == "nan" or df["Disposal Time"][i] == "" or df["Disposal Time"][i] == " " or df["Disposal Time"][i] == None or df["Disposal Time"][i] == 'None' or df["Disposal Time"][i] == "nan":
                            disposal_time = float(0)
                        else:
                            disposal_time_str = str(df["Disposal Time"][i])
                            disposal_time = disposal_time_str.replace(":", ".")
                            if len(disposal_time.split(".")) > 2:
                                disposal_time = float(str(disposal_time.split(
                                    ".")[0] + "." + disposal_time.split(".")[1]))

                        try:
                            train_coach_type = (df["Train Coach Type"][i])
                        except KeyError as e:
                            train_coach_type = "-1"

                        try:
                            physical_coach_number = float(
                                df["Physical Coach No"][i])
                        except KeyError as e:
                            physical_coach_number = "-1"

                        try:
                            physical_coach_type = df["Coach Type"][i]
                        except KeyError as e:
                            physical_coach_type = "-1"

                        try:
                            rake_number = (df["Rake No."][i])
                        except KeyError as e:
                            rake_number = "-1"

                        try:

                            problem_type = (df["Type"][i])

                            if problem_type == "Corruption / Bribery":
                                problem_type = "Corruption Bribery"
                                # main_data.save()

                            elif problem_type == "Catering & Vending Services":
                                problem_type = "Catering and Vending Services"
                        except KeyError as e:
                            messages.error(
                                request, 'Please re-check the data for problem_type')
                            raise ValueError(
                                "Issue while reading problem_type")
                            return redirect(request.path)

                        try:
                            sub_problem_type = (df["Sub Type"][i])
                        except KeyError as e:
                            messages.error(
                                request, 'Please re-check the data for sub problem_type')
                            raise ValueError(
                                "Issue while reading sub problem_type")
                            return redirect(request.path)

                        try:
                            staff_name = (df["Escorting Staff"][i])
                        except KeyError as e:
                            staff_name = "-1"

                        try:
                            owning_zone = (df["Owning Zone"][i])
                        except KeyError as e:
                            owning_zone = "-1"

                        try:
                            owning_div = (df["Owning Div"][i])
                        except KeyError as e:
                            owning_div = "-1"

                        try:
                            dept = (df["Dept"][i])
                        except KeyError as e:
                            dept = "-1"
                        try:
                            train_coach_number = float(
                                df["Train Coach No."][i])
                        except KeyError as e:
                            train_coach_number = "-1"
                        try:
                            upcoming_station = (df["Upcoming Station"][i])
                        except KeyError as e:
                            upcoming_station = "-1"

                        try:
                            mob_email_id = (df["Mobile No./Email Id"][i])
                        except KeyError as e:
                            mob_email_id = "-1"

                        try:
                            train_name = (df["Train Name"][i])
                        except KeyError as e:
                            train_name = "-1"

                        try:
                            current_user_id = (df["Current User Id"][i])
                        except KeyError as e:
                            current_user_id = "-1"

                        try:
                            current_user_mobile_number = (
                                df["Current User Mobile No"][i])
                        except KeyError as e:
                            current_user_mobile_number = "-1"

                        obj, created = Main_Data_Upload.objects.update_or_create(
                            reference_number=reference_number,
                            defaults={
                                "sl_number": sl_number,
                                "reference_number": reference_number,
                                "registration_date": registeration_date,
                                "closing_date": closing_date,
                                "disposal_time": disposal_time,
                                "train_station": df["Train/Station"][i],
                                "train_coach_type": train_coach_type,
                                "physical_coach_number": physical_coach_number,
                                "rake_number": rake_number,
                                "staff_name": staff_name,
                                "problem_type": problem_type,
                                "sub_type": sub_problem_type,
                                "zone": df["Zone"][i],
                                "div": df["Div"][i],
                                "owning_zone": owning_zone,
                                "owning_div": owning_div,
                                "dept": dept,
                                "breach": df["Breach"][i],
                                "rating": df["Rating"][i],
                                "status": df["Status"][i],
                                "complaint_discription": df["Complaint Description"][i],
                                "remark": df["Remarks"][i],
                                "number_of_time_forwarded": df["No. of times forwarded"][i],
                                "pnr_utc_number": df["PNR/UTS No"][i],
                                "physical_coach_type": physical_coach_type,
                                "train_coach_number": train_coach_number,
                                "feedback_remark": df["Feedback Remarks"][i],
                                "upcoming_station": upcoming_station,
                                "mobile_number_or_email": mob_email_id,
                                "train_name": train_name,
                                "current_user_id": current_user_id,
                                "current_user_mobile_number": current_user_mobile_number,
                                "created_at": now,
                                "updated_at": now,
                                "created_by": user,
                                "updated_by": str(request.user.username),
                            }
                        )
                        obj.save()
                    except:
                        # print("Error in saving data")
                        ERROR_REFERENCE_NUMBER.append(reference_number)
                        pass

            except KeyError as e:
                msg_info = f'Please re-check the data Column And Upload Again because there was no reference number in the data field'
                messages.error(request, msg_info)
                return redirect(request.path)

            except Exception as e:
                print(e)
                # reference_number=df["Ref. No."][i]
                msg_info = f'Please re-check the data Column And Upload Again. Problem with the reference number {ERROR_REFERENCE_NUMBER}'
                messages.error(request, msg_info)
                return redirect(request.path)

            # def send_whatsapp_msg():
            #     mobile_number = PhoneNumber.objects.all()
            #     phone_number = []
            #     for m_n in mobile_number:
            #         phone_number.append("whatsapp:+91" + str(m_n))

            #     config = open('./secretes.json')
            #     data = load(config)
            #     account_sid = data["TWILIO_PROD"]["ACCOUNT_SID"]
            #     auth_token = data["TWILIO_PROD"]["AUTH_TOKEN"]
            #     from_phone = data["TWILIO_PROD"]["FROM_PHONE"]
            #     client = Client(account_sid, auth_token)

            #     len_ERROR_REFERENCE_NUMBER = len(ERROR_REFERENCE_NUMBER)
            #     remaining = len_ERROR_REFERENCE_NUMBER
            #     factor = 0
            #     if len_ERROR_REFERENCE_NUMBER > 0:
            #         while remaining >= 10:
            #             whatsapp_msg = f"File has been uploaded and problem with data {str(ERROR_REFERENCE_NUMBER[(10*factor ): ((10*factor) + 10) ])} on the Server--> on date:- {dt_string}"
            #             remaining -= 10
            #             factor += 1
            #             for p_n in phone_number:
            #                 message = client.messages.create(
            #                     body=whatsapp_msg,
            #                     from_=f"whatsapp:{from_phone}",
            #                     to=f"{p_n}",
            #                 )
            #                 time.sleep(1)
            #         if remaining > 0 and remaining < 10:
            #             whatsapp_msg = f"File has been uploaded and problem with data {str(ERROR_REFERENCE_NUMBER)} on the Server--> on date:- {dt_string}"
            #             for p_n in phone_number:
            #                 message = client.messages.create(
            #                     body=whatsapp_msg,
            #                     from_=f"whatsapp:{from_phone}",
            #                     to=f"{p_n}",
            #                 )
            #                 time.sleep(1)

            #         messages.success(
            #             request, f"Data is Uploaded. Problem with data {str(ERROR_REFERENCE_NUMBER)}")
            #     else:
            #         for p_n in phone_number:
            #             message = client.messages.create(
            #                 body=f"File has been uploaded on the Server--> on date:- {dt_string}",
            #                 from_=f"whatsapp:{from_phone}",
            #                 to=f"{p_n}",
            #             )
            #             time.sleep(1)
            #         messages.success(request, f"Data is Uploaded.")
            # send_whatsapp_msg()

            return redirect(request.path)
        else:
            messages.error(request, "You Cannot Upload Data")
            return redirect(request.path)

    return render(request, "railmadad/old_data_upload.html")


###################################################################
