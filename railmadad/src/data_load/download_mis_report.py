# # TODO 
# # This file is looks like a POC file, not needed in prod, 
# # looks like created by Shubham

# from ast import Div
# from email import message
# from pickle import NONE
# from pydoc import resolve
# from sre_parse import CATEGORIES
# from tracemalloc import start
# import operator
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from pip import main
# from app.models import *
# import math
# import more_itertools
# import dateutil.parser
# from django.contrib.auth.decorators import login_required
# from django.db.models import Count
# from django.contrib.auth import login as auth_login
# from django.core.paginator import Paginator, EmptyPage
# from django.contrib.auth.models import *
# from django.db.models import Count
# from operator import itemgetter
# from django.contrib.auth import login, authenticate, logout
# from django.contrib import messages
# import numpy as np
# from email.mime.image import MIMEImage
# import os
# import datetime
# from datetime import datetime as dt
# import calendar
# from django.db.models import Sum
# from matplotlib import pyplot as plt
# import pandas as pd
# import matplotlib
# import csv
# import json
# matplotlib.use("Agg")
# from datetime import date, timedelta
# from dateutil.rrule import rrule, MONTHLY
# import calendar
# from calendar import monthrange
# import datetime as DT
# from django.views.decorators.csrf import csrf_exempt
# import os
# from twilio.rest import Client
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
# import time
# import urllib
# from django.db.models import Sum
# from railmadad.constants import *
# from django.contrib.auth.decorators import login_required



# def upload_file_on_site():
#     driver = webdriver.Chrome(executable_path="./chromedriver.exe")
#     driver.implicitly_wait(0.5)
#     driver.maximize_window()
#     driver.get("http://localhost:8000/railmadad/data_upload")
#     driver.find_element("id", "username").send_keys("shubham")
#     driver.find_element("id", "password").send_keys("1234")
#     driver.find_element(
#         "xpath", "/html/body/section/div/div/div/div/div/div[1]/form/button"
#     ).click()
#     time.sleep(2)
#     driver.execute_script(
#         "arguments[0].scrollIntoView();",
#         driver.find_element(By.ID, "data-upload-click"),
#     )
#     driver.find_element(By.ID, "data-upload-click").click()
#     # to identify element
#     s = driver.find_element("xpath", "//input[@type='file']")
#     # file path specified with send_keys
#     s.send_keys(
#         "D:/Internship/Railway-Project/downloads/annual-enterprise-survey-2021-financial-year-provisional-csv.csv"
#     )
#     driver.find_element(By.ID, "upload-csv").click()
#     time.sleep(300)


# def download_csv(request):
#     if request.method != "POST":
#         return render(request, "download_csv.html")

#     else:
#         driver = webdriver.Chrome(executable_path="chromedriver.exe")
#         driver.implicitly_wait(0.5)
#         _path = (
#             os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\downloads"
#         )
#         chrome_options = webdriver.ChromeOptions()
#         prefs = {"download.default_directory": _path}
#         chrome_options.add_experimental_option("prefs", prefs)
#         chrome_options.add_argument(
#             "--headless"
#         )  # start chrome without opening browser.
#         driver = webdriver.Chrome(
#             executable_path="D:\Railway-Project\chromedriver.exe",
#             options=chrome_options,
#         )
#         driver.get("https://www.stats.govt.nz/large-datasets/csv-files-for-download/")
#         driver.find_element(
#             "xpath",
#             "/html/body/div[12]/div/div/main/section/div/div/div/article/div/div[2]/article/ul/li[1]/div/div/h3/a",
#         ).click()
#         time.sleep(10)
#         driver.quit()
#         upload_file_on_site()
#         return redirect("/railmadad/download_csv")
#         # D:\Internship\Railway-Project\downloads\annual-enterprise-survey-2021-financial-year-provisional-csv.csv


# @login_required
# def download_mis_report(request):
#     key = None
#     if request.method == "POST":
#         from datetime import datetime
#         import requests
#         from requests.structures import CaseInsensitiveDict

#         key = request.POST.get("key")
#         user = User.objects.get(id=request.user.id)
#         if user.groups.filter(name="Moderator").exists():
#             today_date = str(datetime.today().strftime("%Y-%m-%d"))
#             download_url = f"https://railmadad.indianrailways.gov.in/rmmis/AllReportFetchServlet?fetchDataType=report1data&complaintZoneInput=&complaintDivInput=&complaintTypeInput=&complaintSubTypeInput=&complaintModeInput=&refundInput=Y&inquiryInput=Y&complaintDeptInput=&fromInput={today_date}&toInput={today_date}&flag=N&flag1=N&viewType=zoneview"
#             # r=requests.get(download_url, headers={f"Cookie":"JSESSIONID={key}"})
#             headers = CaseInsensitiveDict()
#             headers["Cookie"] = f"JSESSIONID={key}"
#             resp = requests.get(download_url, headers=headers)

#         else:
#             messages.error(request, "You Are Not Moderator")
#             return redirect(request.path)
#     return render(request, "railmadad/download_mis_report.html")
