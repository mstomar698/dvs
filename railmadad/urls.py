from django.shortcuts import redirect
from django.urls import path
from railmadad.src.data_load import download_csv_data_old, download_csv_data_new, load_data_new, load_data_old, add_train_category, add_staff_name, add_physical_coach_number, create_new_staff


from railmadad.src.analytical_features import complain_type_absolute, complain_type_interactive,complain_type_interactive_line_chart, rating_chart, trends_rating, trends, sub_type, train_wise_complaint_mix_chart, staff_graph, physical_coach_number_wise_complain_mix_chart, all_complain_sub_type_train, maximum_complain_train, maximum_complain_coach, rating_chart_with_percentage, train_summary_table, coach_summary_table, disposal_time_coach_wise, disposal_time_date_wise, disposal_time_sub_type_wise, disposal_time_train_wise

from . import views


urlpatterns = [
    path("", lambda request : redirect('trend_rating/') , name="redirect_trend_rating"),
    path('complain_type_absolute_percentage/',
        complain_type_absolute.dashboard, name="dashboard"),
    path('complain/<str:complain>/<str:start_date>/<str:end_date>',
        complain_type_interactive.complain_type, name="complain_type"),
    path('complain/<str:complain>/<str:start_date>/<str:end_date>/<str:clicked_date>',
        complain_type_interactive_line_chart.complain_type_line_chart, name="complain_type_line_chart"),
    path('rating/', rating_chart.rating, name="rating"),
    path('trend_rating/', trends_rating.trend_rating, name="trend_rating"),
    path('trend/', trends.trend, name="trend"),
    path('sub_type/<str:subtype>/', sub_type.sub_type, name="sub_type"),
    path('train_wise_data/', views.train_wise_data, name="train_wise_data"),
    path('bottom_train_data_pie_chart/',
        views.bottom_train_data_pie, name="bottom_train_data_pie"),
    path('bottom_train_data_bar_chart/',
        views.bottom_train_data_bar, name="bottom_train_data_bar"),


    path('all_complain_train/',
        views.all_complain_train, name="all_complain_train"),
    path('all_sub_complain_train/<str:subtype>/',
        all_complain_sub_type_train.all_sub_complain_train, name="all_sub_complain_train"),
    path('max_complain_train/',
        maximum_complain_train.max_complain_train, name="max_complain_train"),
    path('min_complain_train/',
        views.min_complain_train, name="min_complain_coach"),
    path('max_complain_coach/',
        maximum_complain_coach.max_complain_coach, name="max_complain_coach"),
    path('min_complain_coach/',
        views.min_complain_coach, name="min_complain_coach"),
    path('mix_coach_graph/', physical_coach_number_wise_complain_mix_chart.
         mix_coach_graph, name="mix_coach_graph"),
    path('staff_graph/', staff_graph.staff_graph, name="staff_graph"),
    path('mix_chart/', train_wise_complaint_mix_chart.mix_chart, name="mix_chart"),
    path('add_train_cat/',
        add_train_category.add_train_cat, name="add_train_cat"),
    path('add_staff_csv/', add_staff_name.add_staff_csv, name="add_staff_csv"),
    path('show_physical_coach_number/',
        add_physical_coach_number.show_physical_coach_number, name="show_physical_coach_number"),
    path('add_physical_coach_number/',
        add_physical_coach_number.add_physical_coach_number, name="add_physical_coach_number"),
    
    path('show_staff_name/',
         add_staff_name.show_staff_name, name="show_staff_name"),
    path('create_staff/', create_new_staff.create_staff, name="Create Staff"),





    path('rating_percentage/',
        rating_chart_with_percentage.rating_percentage, name="rating_percentage"),

    path('data_upload/', load_data_new.upload_data, name="upload_data"),
    path('old_data_upload/',
        load_data_old.old_upload_data, name="old_upload_data"),

    path('download_data_csv/',
        download_csv_data_new.download_data_csv, name="session_key"),
    path('old_download_data_csv/',
        download_csv_data_old.old_download_data_csv, name="session_key"),

    # path('download_csv/', download_mis_report.download_csv, name="download_csv"),
    # path('download_mis_report/',
    #     download_mis_report.download_mis_report, name="session_key"),

    path('train_summary_table/',
        train_summary_table.train_summary_table, name="train_summary_table"),
    path('coach_summary_table/',
        coach_summary_table.coach_summary_table, name="coach_summary_table"),
    # path('coach_num_wise_data/', views.physical_coach_number_wise_data, name="coach_num"),
    path('disposal_time_date_wise/',
        disposal_time_date_wise.disposal_time_date_wise, name="disposal_time_date_wise"),
    path('disposal_time_train_wise/',
        disposal_time_train_wise.disposal_time_train_wise, name="disposal_time_train_wise"),
    path('disposal_time_coach_wise/',
        disposal_time_coach_wise.disposal_time_coach_wise, name="disposal_time_coach_wise"),
    path('disposal_time_sub_type_wise/',
        disposal_time_sub_type_wise.disposal_time_sub_type_wise, name="disposal_time_sub_type")
]
