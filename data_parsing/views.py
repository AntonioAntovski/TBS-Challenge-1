# Create your views here.
from mongoengine import connect, disconnect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from data_parsing.helper_functions import insert_into_db
from data_parsing.models import Candidate
from data_parsing.transform_candidates import transform_candidates


@api_view(['POST'])
@permission_classes((AllowAny,))
def parse_data(request):
    data_json = request.data

    if not data_json:
        return Response({'message': 'No data sent. Try again.'}, status=400)

    for obj in data_json:
        insert_into_db(obj)

    return Response({'message': 'The data was inserted into db successfully.'}, status=200)


@api_view(['POST'])
@permission_classes((AllowAny,))
def query_data(request):
    connect("challenge1",
            host="127.0.0.1",
            port=27017,
            username="antonio",
            password="Antonio123")

    query_json = request.data

    job_title = query_json.get('job_title', None)
    job_dates = query_json.get('job_dates', None)
    job_description = query_json.get('job_description', None)
    location = query_json.get('location', None)

    if job_title:
        candidates = Candidate.objects.filter(jobs__title=job_title)
    else:
        candidates = Candidate.objects.all()

    if job_dates:
        start = job_dates.get('start', None)
        end = job_dates.get('end', None)

        if start:
            candidates = candidates.filter(jobs__start__gte=start)
        if end:
            candidates = candidates.filter(jobs__start__lte=start)

    if job_description:
        candidates = candidates.filter(jobs__description=job_description)

    if location:
        city = location.split('.')[0].strip()
        country = location.split('.')[1].strip()

        candidates = candidates.filter(locations__city=city, locations__country=country)

    disconnect()

    return Response(transform_candidates(candidates), status=200)
