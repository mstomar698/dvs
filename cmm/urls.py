from django.shortcuts import redirect
from django.urls import path

from . import views
from cmm.src.data_upload.upload_data_sick_head import upload_data_sick_head
from cmm.src.data_upload.upload_data_pro import upload_data_pro
from cmm.src.data_upload.upload_data_warranty_complain_new import upload_data_warranty_complain_new
from cmm.src.data_upload.upload_data_warranty_complain import upload_data_warranty_complain

urlpatterns = [
    path('', lambda request: redirect('sick_head_graph/'), name="redirect_sick_head_graph"),
    path('data_upload_sick_head/', upload_data_sick_head, name="upload_data"),
    path('data_upload_warranty_complain/', upload_data_warranty_complain, name="upload_data1"),
    path('data_upload_pro/', upload_data_pro, name="upload_data_pro"),
    path('sick_head_graph/', views.sick_head_graph, name="sick_head_graph"),
    path('sick_head_table/', views.sick_head_table, name="sick_head_table"),
    path('sick_head_multiple/', views.sick_head_multiple, name="sick_head_table"),
    path('warranty_complain_graph/', views.warranty_complain_graph, name="warranty_complain_graph"),
    path('coach_pro_table/', views.coach_pro_table, name="coach_pro_table"),
    path('complain/<str:complain>/<str:problem_start>/<str:problem_end>', views.complain_type, name="complain_type"),
    path('complain/<str:complain>', views.complain, name="complain"),
    path('coach_pro_query/<str:coach_number_id>', views.coach_pro_query, name="coach_pro_query"),



    ## Download CSV ###
    path('download_sick_head_data_csv/', views.download_sick_head_data_csv, name="download_sick_head_data_csv"),
    path('download_helper/', views.download_helper, name="download_data_csv"),


    path('download_warranty_complain_data_csv/', views.download_warranty_complain_data_csv, name="download_warranty_complain_data_csv"),
    path('download_warranty_helper/', views.download_warranty_helper, name="download_warranty_complain_data_csv"),

    path('download_data_csv_PRO/', views.download_data_csv_PRO, name="download_data_csv"),
    path('download_helper_PRO/', views.download_helper_PRO, name="download_data_csv"),


    path('data_upload_warranty_complain_new/', upload_data_warranty_complain_new, name="data_upload_warranty_complain_new"),
    path('download_warranty_complain_data_new_csv', views.download_warranty_complain_data_new_csv, name="download_warranty_complain_data_new_csv"),
    path('new_warranty_complain_graph/', views.new_warranty_complain_graph, name="new_warranty_complain_graph"),
    path('download_warranty_helper_new/', views.download_warranty_helper_new, name="download_warranty_helper_new"),
    path('new_complain_warranty/<str:complain>/<str:complain_start>/<str:complain_end>', views.new_complain_warranty, name="new_complain_warranty"),
    path('complain_warranty/<str:complain>/<str:complain_start>/<str:complain_end>', views.complain_warranty, name="complain_warranty"),

]
