from django.db import models
from django.contrib.auth.models import User
from .constants import train_types, department





class Main_Data_Upload(models.Model):
    unique_id = models.FloatField(default=None, null=True, blank=True)
    sl_number = models.CharField(max_length=100,
                            default="-1", null=True, blank=True)
    reference_number = models.CharField(max_length=100, unique=True, primary_key=True)
    registration_date = models.DateTimeField(
        default=None, null=True, blank=True)
    closing_date = models.DateTimeField(default=None, null=True, blank=True)
    disposal_time = models.FloatField(default=None, null=True, blank=True)
    mode = models.CharField(max_length=1000,
                            default=None, null=True, blank=True)
    train_station = models.FloatField(null=True, blank=True)
    station_name = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    channel = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    Type = models.CharField(max_length=1000,
                            default=None, null=True, blank=True)
    rake_number = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    staff_name = models.CharField(
        max_length=1000, default="", null=True, blank=True)
    staff_id = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    department = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    problem_type = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    sub_type = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    commodity = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    zone = models.CharField(max_length=1000,
                            default=None, null=True, blank=True)
    div = models.CharField(max_length=1000,
                            default=None, null=True, blank=True)
    dept = models.CharField(max_length=1000,
                            default=None, null=True, blank=True)
    breach = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    rating = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    status = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    complaint_discription = models.TextField(
        default=None, null=True, blank=True)
    remark = models.TextField(default=None, null=True, blank=True)
    number_of_time_forwarded = models.FloatField(
        default=None, null=True, blank=True)
    pnr_utc_number = models.CharField(
        max_length=10000, default=None, null=True, blank=True)
    train_coach_number = models.CharField(
        max_length=10000, default=None, null=True, blank=True)
    feedback_remark = models.TextField(
        default=None, null=True, blank=True)
    upcoming_station = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    mobile_number_or_email = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    current_user_mobile_number = models.CharField(
        max_length=20, default=None, null=True, blank=True)

    train_coach_type = models.CharField(
        max_length=100, default=None, null=True, blank=True)

    
    physical_coach_number = models.FloatField(
        default=00.0, null=True, blank=True)  
    
    physical_coach_type = models.CharField(
        max_length=100, default=None, null=True, blank=True)
    train_name = models.CharField(
        max_length=1000, default=None, null=True, blank=True)

    owning_zone = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    owning_div = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    current_user_id = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    current_user_phone_number = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    dept = models.CharField(
        max_length=1000, default=None, null=True, blank=True)

    created_at = models.DateTimeField(default=None, null=True, blank=True)
    updated_at = models.DateTimeField(default=None, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    updated_by = models.CharField(
        max_length=1000, default=None, null=True, blank=True)

    def __str__(self):
        return str(int(self.reference_number))







class MIS_DATA(models.Model):
    ob = models.FloatField(default=None, null=True, blank=True),
    recv = models.FloatField(default=None, null=True, blank=True),
    settled = models.FloatField(default=None, null=True, blank=True),
    cb = models.FloatField(default=None, null=True, blank=True),
    avgRating = models.FloatField(default=None, null=True, blank=True),
    deptCode = models.CharField(
        max_length=100000, default=None, null=True, blank=True),
    deptName = models.CharField(
        max_length=100000, default=None, null=True, blank=True),
    pname = models.CharField(max_length=100000,
                             default=None, null=True, blank=True),
    pid = models.FloatField(default=None, null=True, blank=True),
    sname = models.CharField(max_length=100000,
                             default=None, null=True, blank=True),
    avgDiff = models.FloatField(default=None, null=True, blank=True),
    pendencyDiffCount = models.FloatField(default=None, null=True, blank=True),
    avgPendencyDiff = models.FloatField(default=None, null=True, blank=True),
    mainClosure = models.FloatField(default=None, null=True, blank=True),
    org = models.CharField(max_length=100000,
                           default=None, null=True, blank=True),
    avgFrtDiff = models.FloatField(default=None, null=True, blank=True),
    znCode = models.CharField(max_length=100000,
                              default=None, null=True, blank=True),
    znName = models.CharField(max_length=100000,
                              default=None, null=True, blank=True),
    divCode = models.CharField(
        max_length=100000, default=None, null=True, blank=True),
    divName = models.CharField(
        max_length=100000, default=None, null=True, blank=True),
    compmode = models.CharField(
        max_length=100000, default=None, null=True, blank=True),
    perShare = models.FloatField(default=None, null=True, blank=True),
    perDisposal = models.FloatField(default=None, null=True, blank=True),
    avgDiffName = models.FloatField(default=None, null=True, blank=True),
    ratingName = models.FloatField(default=None, null=True, blank=True),
    avgPendencyDiffName = models.FloatField(
        default=None, null=True, blank=True),
    avgFrtDiffName = models.FloatField(default=None, null=True, blank=True)

    def __str__(self):
        return str(self.sname)

class Train_Type(models.Model):
    train_number = models.IntegerField(default=None, null=True, blank=True)
    Type = models.CharField(choices=train_types, default=None, max_length=200)

    def __str__(self):
        return (str(self.train_number)+"------>"+str(self.Type))


class Staff_Detail(models.Model):
    staff_first_name = models.CharField(
        max_length=10000, default=None, null=True, blank=True)
    staff_last_name = models.CharField(
        max_length=10000, default=None, null=True, blank=True)
    staff_id = models.CharField(
        max_length=1000, default=None, null=True, blank=True)
    department = models.CharField(
        choices=department, default=None, max_length=200)

    def __str__(self):
        return (str(self.staff_id) + "" + str(self.staff_first_name)+" "+str(self.staff_last_name)+"------->"+str(self.department))

class CsvFile(models.Model):
    csv_drive_url_path = models.CharField(max_length=1000, default=None, null=True, blank=True)

    def __str__(self):
        return str(self.csv_drive_url_path)