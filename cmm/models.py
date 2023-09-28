from django.db import models
from django.contrib.auth.models import User

from .constants import owning_rail, department, ac_flag, coach_cat, veh_type, wrk_shop


class Cmm_Sick(models.Model):
    unique_id = models.FloatField(default=None, null=True, blank=True)
    sl_no = models.FloatField(default=None, null=True, blank=True)
    owning_rly = models.CharField(choices=owning_rail, default=None, max_length=200)
    coach_number =models.FloatField(default=00000.0,null=True, blank=True)
    coach_type = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    sick_head = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    cause_of_sick_marking = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    reported_defect = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    work_done = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    problem_date = models.DateTimeField(default=None,null=True, blank=True)
    placement_date = models.DateTimeField(default=None,null=True, blank=True)
    fit_date = models.DateTimeField(default=None,null=True, blank=True)
    coach_status = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    department = models.CharField(choices= department, default=None, max_length=200)
    POH_date = models.DateField(default=None,null=True, blank=True)
    IOH_date = models.DateField(default=None,null=True, blank=True)
    ac_flag = models.CharField(choices= ac_flag, default=None, max_length=200)
    coach_category = models.CharField(choices= coach_cat, default=None, max_length=200)
    vehicle_type = models.CharField(choices= veh_type, default=None, max_length=200)
    train_number = models.FloatField(default=00000.0,null=True, blank=True)
    main_depot = models.CharField(null=True, blank=True,default=None, max_length=200)
    workshop = models.CharField(choices= wrk_shop, default=None, max_length=200)
    sick_head_failed_assembly_position = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    sub_sick_head_failed_sub_assembly = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    sub_sick_head_position_failed_sub_assembly_position = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    failed_assembly_make = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    failed_sub_assembly_make = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    
    #######
    created_at = models.DateTimeField(default=None,null=True, blank=True)
    updated_at = models.DateTimeField(default=None,null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None,null=True, blank=True)
    updated_by = models.CharField(max_length=10000000,default=None, null=True, blank=True)


    def __str__(self):
        return f"{self.sick_head} ------> {self.coach_number}"





class Cmm_pro(models.Model):
    unique_id = models.FloatField(default=None, null=True, blank=True)
    sl_no = models.FloatField(default=None, null=True, blank=True)
    owning_rly = models.CharField(choices=owning_rail, default=None, max_length=200)
    coach_number = models.FloatField(default=00000.0,null=True, blank=True)
    coach_type = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    coach_category = models.CharField(choices= coach_cat, default=None,null=True, max_length=200)
    ac_flag = models.CharField(choices= ac_flag, default=None,null=True, max_length=200)
    guage = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    POH_date = models.DateField(default=None,null=True, blank=True)
    return_date = models.DateField(default=None,null=True, blank=True)
    POH_work = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    IOH_date = models.DateField(default=None,null=True, blank=True)
    IOH_location = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    expected_IOH_date = models.DateField(default=None,null=True, blank=True)
    extend_return_date = models.DateField(default=None,null=True, blank=True)
    manufacture = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    nominated_workshop = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    built_year =  models.IntegerField(default=0,null=True, blank=True)
    base_depot = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    main_depot = models.CharField(null=True, blank=True,default=None, max_length=200)
    main_division = models.CharField(null=True, blank=True,default=None, max_length=200)
    main_railway = models.CharField(null=True, blank=True,default=None, max_length=200)
    last_updated_time = models.DateField(default=None,null=True, blank=True)
    last_updated_by = models.CharField(null=True, blank=True,default=None, max_length=200)

    
    #######
    created_at = models.DateTimeField(default=None,null=True, blank=True)
    updated_at = models.DateTimeField(default=None,null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None,null=True, blank=True)
    updated_by = models.CharField(max_length=10000000,default=None, null=True, blank=True)


    def __str__(self):
        return  f"{self.coach_number}"


class Cmm_Warranty(models.Model):
    unique_id = models.FloatField(default=None, null=True, blank=True)
    sl_no = models.FloatField(default=None, null=True, blank=True)
    complaint_id = models.FloatField(default=None, null=True, blank=True)
    owning_rly = models.CharField(choices=owning_rail, default=None, max_length=2000)
    coach_number = models.FloatField(default=00000.0,null=True, blank=True)
    coach_type = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    factory_tumont_date = models.DateField(default=None,null=True, blank=True)
    complain_by_depot = models.CharField(null=True, blank=True,default=None, max_length=2000)
    complain_by_division = models.CharField(null=True, blank=True,default=None, max_length=2000)
    complain_by_zone = models.CharField(null=True, blank=True,default=None, max_length=2000)
    failed_assembly = models.CharField(null=True, blank=True,default=None, max_length=2000)
    failure_description = models.CharField(null=True, blank=True,default=None, max_length=2000)
    assembly_manufacture = models.CharField(null=True, blank=True,default=None, max_length=2000)
    failure_date = models.DateField(default=None,null=True, blank=True)
    complain_date = models.DateField(default=None,null=True, blank=True)
    complain_status = models.CharField(null=True, blank=True,default=None, max_length=2000)
    responsible_pu_workshop = models.CharField(null=True, blank=True,default=None, max_length=2000)
    closing_date_pu_workshop = models.DateTimeField(default=None,null=True, blank=True)
    remark_by_pu_workshop = models.CharField(null=True, blank=True,default=None, max_length=2000)
    closing_date_by_depot = models.DateTimeField(default=None,null=True, blank=True)
    remark_by_depot = models.CharField(null=True, blank=True,default=None, max_length=2000)
    complaint_name = models.CharField(null=True, blank=True,default=None, max_length=2000)
    designation = models.CharField(null=True, blank=True,default=None, max_length=2000)
    location = models.CharField(null=True, blank=True,default=None, max_length=2000)
    mobile = models.CharField(null=True, blank=True,default=None, max_length=2000)
    email_id = models.CharField(null=True, blank=True,default=None, max_length=2000)
    address = models.CharField(null=True, blank=True,default=None, max_length=2000)
    city = models.CharField(null=True, blank=True,default=None, max_length=2000)


    #######
    created_at = models.DateTimeField(default=None,null=True, blank=True)
    updated_at = models.DateTimeField(default=None,null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None,null=True, blank=True)
    updated_by = models.CharField(max_length=10000000,default=None, null=True, blank=True)


    def __str__(self):
        return f"{self.complaint_id} ------> {self.coach_number}"
    

class Cmm_Warranty_New(models.Model):
    unique_id = models.FloatField(default=None, null=True, blank=True)
    sl_no = models.FloatField(default=None, null=True, blank=True)
    complaint_id = models.FloatField(default=None, null=True, blank=True)
    complain_by_zone = models.CharField(null=True, blank=True,default=None, max_length=2000)
    complain_by_division = models.CharField(null=True, blank=True,default=None, max_length=2000)
    complain_by_depot = models.CharField(null=True, blank=True,default=None, max_length=2000)
    consignee_code= models.FloatField(default=None, null=True, blank=True)
    complaint_to = models.CharField(null=True, blank=True,default=None, max_length=2000)
    owning_rly = models.CharField(choices=owning_rail, default=None, max_length=2000)
    coach_number = models.FloatField(default=00000.0,null=True, blank=True)
    coach_type = models.CharField(max_length=10000000,default=None, null=True, blank=True)
    failed_assembly = models.CharField(null=True, blank=True,default=None, max_length=2000)
    assembly_manufacture = models.CharField(null=True, blank=True,default=None, max_length=2000)
    assembly_srno= models.CharField(null=True, blank=True,default=None, max_length=2000)
    assembly_plno= models.FloatField(default=None, null=True, blank=True)
    assembly_mfg_date = models.DateField(default=None,null=True, blank=True)
    failure_date = models.DateField(default=None,null=True, blank=True)
    failure_description = models.CharField(null=True, blank=True,default=None, max_length=2000)
    complain_date = models.DateField(default=None,null=True, blank=True)
    complain_status = models.CharField(null=True, blank=True,default=None, max_length=2000)
    depot_remarks = models.CharField(null=True, blank=True,default=None, max_length=2000)
    div_remarks = models.CharField(null=True, blank=True,default=None, max_length=2000)
    pu_ws_remarks = models.CharField(null=True, blank=True,default=None, max_length=2000)
    udm_remarks = models.CharField(null=True, blank=True,default=None, max_length=2000)
    udm_date = models.DateField(default=None,null=True, blank=True)
    pu_ws_date = models.DateField(default=None,null=True, blank=True)
    div_date = models.DateField(default=None,null=True, blank=True)
    complain_by_mobile = models.CharField(null=True, blank=True,default=None, max_length=2000)

    #######
    created_at = models.DateTimeField(default=None,null=True, blank=True)
    updated_at = models.DateTimeField(default=None,null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None,null=True, blank=True)
    updated_by = models.CharField(max_length=10000000,default=None, null=True, blank=True)


    def __str__(self):
        return f"{self.complaint_id} ------> {self.coach_number}"
    
class Failed_Assembly(models.Model):
    failed_id= models.FloatField(default=None, null=True, blank=True)
    failed_item= models.CharField(null=True, blank=True,default=None, max_length=2000)

class Complaint_numbers(models.Model):
    complaint_id=models.FloatField(default=None, null=True, blank=True)

class CsvFile(models.Model):
    csv_drive_url_path = models.CharField(max_length=1000, default=None, null=True, blank=True)

    def __str__(self):
        return str(self.csv_drive_url_path)
