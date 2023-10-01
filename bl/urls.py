
# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # data APIs
    path('pie_chart_country/', views.pie_chart_country, name='pie_chart_country'),#GET REVERTING #POST
    path('pie_chart_region/', views.pie_chart_region, name='pie_chart_region'),#POST REVERTING #GET
    path('bar_graph_Source/', views.bar_graph_Source, name='bar_graph_Source'),#GET
    path('pie_chart_pestle/', views.pie_chart_pestle, name='pie_chart_pestle'),#GET
    path('dot_graph_pestle_sector_inetnsity/', views.dot_graph_pestle_sector_inetnsity, name='dot_graph_pestle_sector_inetnsity'),#POST
    path('pie_chart_sector/', views.pie_chart_sector, name='pie_chart_sector'),#GET
    path('dot_graph_sector_topic_relevance/', views.dot_graph_sector_topic_relevance, name='dot_graph_sector_topic_relevance'),#POST
    path('bar_graph_sector_topic_likelihood/', views.bar_graph_sector_topic_likelihood, name='bar_graph_sector_topic_likelihood'),#GET
    path('table_topic_insights_details/', views.table_topic_insights_details, name='table_topic_insights_details'),#POST
    path('dot_graph_for_insights_published_date/', views.dot_graph_for_insights_published_date, name='dot_graph_for_insights_published_date'),#GET

    # home
    path('home/', views.home, name='home'),#GET
    path('api/csrf/', views.get_csrf_token, name='get_csrf_token'),#GET
]