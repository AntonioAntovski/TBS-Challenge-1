from mongoengine import connect, disconnect
import base64
import re
from data_parsing.models import Job, Skill, Location, Candidate
import xml.etree.ElementTree as ET
from datetime import datetime


def parse_birth_date(date_string):
    month_to_number = {
        'jan': '01',
        'feb': '02',
        'mar': '03',
        'apr': '04',
        'may': '05',
        'jun': '06',
        'jul': '07',
        'aug': '08',
        'sep': '09',
        'oct': '10',
        'nov': '11',
        'dec': '12'
    }

    if not date_string:
        return None

    parts = date_string.split()

    day = re.sub(r'(st)|(nd)|(rd)|(th)', '', parts[0])
    month = month_to_number.get(parts[1][:3].lower(), parts[1])
    year = parts[2]

    if len(day) == 1:
        day = f"0{day}"

    return datetime.fromisoformat(f"{year}-{month}-{day}")


def parse_job_date(date_string):
    parts = date_string.split('/')
    return datetime.fromisoformat(f"20{parts[0]}-{parts[2]}-{parts[1]}")


def decode_job(string):
    string_bytes = string.encode('ascii')
    string_bytes_d = base64.b64decode(string_bytes)
    xml_string = string_bytes_d.decode('ascii')

    if xml_string.startswith('<'):

        xml_string = re.sub(r'^[^\s*\<.*$].*', '', xml_string).strip()

        xml_obj = ET.fromstring(xml_string)

        job_title = xml_obj.find('title').text
        start = parse_job_date(xml_obj.find('started_at').text)
        end = parse_job_date(xml_obj.find('finished_at').text)
        description = xml_obj.find('description').text

        job = Job(
            title=job_title,
            start=start,
            end=end,
            description=description
        )

        return job


def parse_skill(string):
    parts = string.split('\n')[1]

    name = parts.split(',')[0].strip()
    obtained = datetime.fromisoformat(f"{parts.split(',')[1].strip()}-01-01")

    skill = Skill(
        name=name,
        obtained=obtained
    )

    return skill


def insert_into_db(obj):
    connect("challenge1",
            host="127.0.0.1",
            port=27017,
            username="antonio",
            password="Antonio123")

    name = obj.get('name', None)
    birth_date = parse_birth_date(obj.get('birth_date', None))
    locations = obj.get('locations', None)
    jobs = obj.get('jobs', [])
    skills = obj.get('skills', [])

    if locations:
        if len(re.split('\. |,', locations)) > 1:
            locations = [
                Location(
                    city=location.split('.')[0].strip(),
                    country=location.split('.')[1].strip()
                )
                for location in locations.split(', ')]
        else:
            locations = None

    if jobs:
        jobs_ = []
        for string in jobs:
            job = decode_job(string)
            if job:
                jobs_.append(job)

        jobs = jobs_

    if skills:
        skills = [parse_skill(string) for string in skills]

    candidate = Candidate(
        name=name,
        birth_date=birth_date,
        locations=locations,
        jobs=jobs,
        skills=skills
    ).save()

    disconnect()
