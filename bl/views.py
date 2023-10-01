# views.py

from collections import defaultdict
import json
from django.http import JsonResponse
import random
from django.shortcuts import render
from requests import Response
from rest_framework.decorators import api_view
from datetime import datetime
from pytz import timezone, utc

from bl.models import ArticleDetails
from bl.serializers import ArticleDetailsSerializer
from django.db.models.functions import Coalesce
from django.db.models import Sum, F, Q, Min, Max, Avg, Count

@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = request.COOKIES.get('csrftoken')
    print(csrf_token)
    return JsonResponse({'csrfToken': csrf_token})

@api_view(['GET'])
def home(request):
    articles = ArticleDetails.objects.all()
    # serializer = ArticleDetailsSerializer(articles, many=True)
    # filtered_data = serializer.data
    message = 'Get APIs working, backend connected'
    return JsonResponse({'message': message}, safe=False)


@api_view(['POST'])
def pie_chart_country(request):
    all_data = ArticleDetails.objects.all()
    region_clicked = request.POST.get("region")
    # we require to check if data have country field, than count all the data respective to each country and make a dictionery with item as country and value as count in as how many times articles is published or added from that country, and lastly send the data as JSON so that we can use it in react.  
    country_data = defaultdict(int)
    for data in all_data:
        # Check if the country is empty or ""
        if data.region == region_clicked:
            if not data.country:
                country_name = "unverified"
            else:
                country_name = data.country
            
            country_data[country_name] += 1
    country_data = dict(country_data)

    return JsonResponse(country_data)

@api_view(['GET'])
def pie_chart_region(request):
    all_data = ArticleDetails.objects.all()
    
    # now, just as the country clicked by user, search DB for all articles with same country and collect all reagions in that country. Similarly as we renamed "" as unverified, now do the same for region entry with "" as unverified and "World" as "All"  
    region_data = defaultdict(int)

    for data in all_data:
        # Check if the region is empty or "World" and rename as "All"
        if data.region == "World":
            region_name = "All"
        elif not data.region:
            region_name = "unverified"
        else:
            region_name = data.region

        region_data[region_name] += 1

    region_data = dict(region_data)

    return JsonResponse(region_data)

@api_view(['GET'])
def bar_graph_Source(request):
    all_data = ArticleDetails.objects.all()
    # we require to check if data have country field, than count all the data respective to each country and make a dictionery with item as country and value as count in as how many times articles is published or added from that country, and lastly send the data as JSON so that we can use it in react.  
    source_data = defaultdict(int)
    
    for data in all_data:
        # Check if the country is empty or ""
        if not data.source:
            source_name = "unverified"
        else:
            source_name = data.source
        
        source_data[source_name] += 1

    source_data = dict(source_data)

    return JsonResponse(source_data)


@api_view(['GET'])
def pie_chart_pestle(request):
    all_data = ArticleDetails.objects.all()

    # Initialize a defaultdict to count articles per pestle
    pestle_data = defaultdict(int)

    for data in all_data:
        # Check if the pestle is empty or ""
        if not data.pestle:
            pestle_name = "unrelated"
        else:
            pestle_name = data.pestle

        pestle_data[pestle_name] += 1

    # Convert the defaultdict to a regular dictionary
    pestle_data = dict(pestle_data)

    # Serialize the dictionary to JSON and return it using JsonResponse
    return JsonResponse(pestle_data)
    

@api_view(['POST'])
def dot_graph_pestle_sector_inetnsity(request):
    pestle_selected = request.POST.get('pestle')
    # for the selected pestle from post req. we will create a dot graph with fields intensity, and sceor that pestle is intensifying.
    # so we will need a logic that sends sector and intensity data over the duration of article publishment, 
    # like article published 17 th jan 2017 for sector of Energy in Industries pestle and have intensity of 4 similarly all other sectors on that day published will show there respective intensities.
    articles = ArticleDetails.objects.filter(pestle=pestle_selected)
    # print(pestle_selected)
    # Group articles by date, sector, and calculate the sum of intensity
    grouped_data = articles.values('published__date', 'added__date', 'sector').annotate(
        intensity_sum=Avg(Coalesce('intensity', 0))
    )

    # Prepare data for the dot graph
    dot_graph_data = {}
    for entry in grouped_data:
        date = entry['published__date'] or entry['added__date']  # Use published date, if available, else added date
        date_str = date.strftime('%Y-%m-%d')  # Convert date to string
        if not entry['sector']:
            sector = "unrelated"
        else:
            sector = entry['sector']
        intensity_sum = round(entry['intensity_sum'])

        if date_str not in dot_graph_data:
            dot_graph_data[date_str] = []

        dot_graph_data[date_str].append({'sector': sector, 'intensity_sum': intensity_sum})

    return JsonResponse(dot_graph_data)


@api_view(['GET']) # no UI as we are using intensity ui for secore in each pestle
def pie_chart_sector(request):
    all_data = ArticleDetails.objects.all()

    # Initialize a defaultdict to count articles per pestle
    sector_data = defaultdict(int)

    for data in all_data:
        # Check if the pestle is empty or ""
        if not data.sector:
            sector_name = "unrelated"
        else:
            sector_name = data.sector

        sector_data[sector_name] += 1

    # Convert the defaultdict to a regular dictionary
    sector_data = dict(sector_data)

    # Serialize the dictionary to JSON and return it using JsonResponse
    return JsonResponse(sector_data)
    

@api_view(['POST'])
def dot_graph_sector_topic_relevance(request):
    sector_selected = request.POST.get('sector')
    # Filter articles based on the selected sector
    articles = ArticleDetails.objects.filter(sector=sector_selected)

    # Group articles by date, sector, and calculate the sum of intensity
    grouped_data = articles.values('published__date', 'added__date', 'topic').annotate(
        relevance_sum=Sum(Coalesce('relevance', 0))
    )

    # Prepare data for the dot graph
    dot_graph_data = {}
    for entry in grouped_data:
        date = entry['published__date'] or entry['added__date']  # Use published date, if available, else added date
        date_str = date.strftime('%Y-%m-%d')  # Convert date to string
        topic = entry['topic']
        relevance_sum = entry['relevance_sum']

        if date_str not in dot_graph_data:
            dot_graph_data[date_str] = []

        dot_graph_data[date_str].append({'topic': topic, 'relevance_sum': relevance_sum})

    return JsonResponse(dot_graph_data)


@api_view(['GET'])
def bar_graph_sector_topic_likelihood(request):
    all_data = ArticleDetails.objects.all()
    # Ok, now we just have to group sector, topic and likelihood of arriving of each topic corresponding to its sector
    # Like, for Energy sector, likelihood of gas is 3 for insight  "Annual Energy Outlook" is 3. 
    # so we for each sector we will collect all availabale topics and then for all available topics we will calulate average of likelihood as likelihood must not go more than 4 for average too!! so round off to nearelst larger number for average.
    # also for not mentioned sectors i.e. "" we will name it as unrelated. 
    # Group articles by sector and topic, and calculate the average likelihood
    grouped_data = ArticleDetails.objects.values('sector', 'topic').annotate(
        avg_likelihood=Avg('likelihood')
    )

    # Prepare data for the bar graph
    bar_graph_data = {}
    for entry in grouped_data:
        sector = entry['sector'] or 'Unrelated'
        topic = entry['topic'] or 'not_mentioned'  # Rename empty topic to 'not_mentioned'
        avg_likelihood = entry['avg_likelihood']

        if sector not in bar_graph_data:
            bar_graph_data[sector] = []

        # Round the average likelihood to the nearest larger integer
        avg_likelihood = round(avg_likelihood)
        bar_graph_data[sector].append({'topic': topic, 'avg_likelihood': avg_likelihood})

    return JsonResponse(bar_graph_data)


@api_view(['POST'])
def table_topic_insights_details(request):
    sector_clicked = request.POST.get('sector')
    topic_clicked = request.POST.get('topic')
    # when user provides sector and and topic, we will a show a table with all insights that relates to the topic in the corresponding sector, the table will have following fields: Insight, url, title, source, start Year and  end Year for each of the respective insight since it is not same for any field. add logic so that we can pass all requested data in JSON to the frontend. enlist sector and topic for which we are collecting data.
    articles = ArticleDetails.objects.filter(sector=sector_clicked, topic=topic_clicked)
    # Prepare data for the table
    table_data = []
    for article in articles:
        table_data.append({
            'insight': article.insight,
            'url': article.url,
            'title': article.title,
            'source': article.source,
            'start_year': article.start_year,
            'end_year': article.end_year,
        })

    # Create a dictionary containing sector and topic information along with the table data
    response_data = {
        'sector': sector_clicked,
        'topic': topic_clicked,
        'table_data': table_data,
    }

    return JsonResponse(response_data)


@api_view(['GET'])
def dot_graph_for_insights_published_date(request):
    # here we just have to show all the articles with published or added date, so group all the data according to published or added date, corresponding to insight and attach topic with it in correspondence to insight. 
    # put logic such that I get JSON data for this req.
     # Group articles by published or added date, insight, and topic
    # Group articles by published or added date and prepare data for the dot graph
    grouped_data = ArticleDetails.objects.values('added', 'published', 'insight', 'title')

    # Create a dictionary to group insights by date
    dot_graph_data = defaultdict(list)
    for entry in grouped_data:
        date = entry['published'] or entry['added']  # Use published date if available, else added date
        insight = entry['insight']
        title = entry['title']

        # Limit insight length to the first 20 words (with ellipsis if it exceeds 20 words)
        if len(insight) > 30:
            insight = insight[:30] + '...'

        # Append the insight to the corresponding date
        dot_graph_data[date.strftime('%Y-%m-%d')].append({
            'insight': insight,
            'title': title,
        })

    return JsonResponse(dict(dot_graph_data))


# {
#   "end_year": "",❌☑️✔️
#   "intensity": 6,✅
#   "sector": "Energy",✅✔️☑️✔️
#   "topic": "gas",✅☑️✔️
#   "insight": "Annual Energy Outlook",✅☑️✔️✅
#   "url": "http://www.eia.gov/outlooks/aeo/pdf/0383(2017).pdf",☑️✔️
#   "region": "Northern America", ✅
#   "start_year": "",❌☑️✔️
#   "impact": "",❌❌❌❌
#   "added": "January, 20 2017 03:51:25", ❌✅
#   "published": "January, 09 2017 00:00:00",❌✅
#   "country": "United States of America", ✅
#   "relevance": 2,✅
#   "pestle": "Industries",✅
#   "source": "EIA",✅☑️✔️
#   "title": "U.S. natural gas consumption is expected to increase during much of the projection period.",☑️✔️✅
#   "likelihood": 3✅
# },

