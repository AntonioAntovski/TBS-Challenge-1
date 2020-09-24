from mongoengine import *


# Create your models here.
class Skill(EmbeddedDocument):
    name = StringField(max_length=255)
    obtained = DateField()

    meta = {
        'indexes': [
            'name',
            'obtained'
        ]
    }


class Job(EmbeddedDocument):
    title = StringField(max_length=255)
    start = DateField()
    end = DateField()
    description = StringField(max_length=255)

    meta = {
        'indexes': [
            'title',
            'start',
            'end',
            'description'
        ]
    }


class Location(EmbeddedDocument):
    city = StringField(max_length=255)
    country = StringField(max_length=255)

    meta = {
        'indexes': [
            'city',
            'country'
        ]
    }


class Candidate(Document):
    name = StringField(max_length=255)
    birth_date = DateField()
    locations = ListField(EmbeddedDocumentField(Location))
    jobs = ListField(EmbeddedDocumentField(Job))
    skills = ListField(EmbeddedDocumentField(Skill))

    meta = {
        'indexes': [
            'name',
            'birth_date',
            'locations',
            'jobs',
            'skills'
        ]
    }
