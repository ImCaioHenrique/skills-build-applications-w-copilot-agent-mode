from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from django.conf import settings

from pymongo import MongoClient

# Models for demonstration (should be in models.py in a real app)
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    user = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    duration = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clean up collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index for email
        db.users.create_index([('email', 1)], unique=True)

        # Teams
        marvel = {'name': 'Marvel'}
        dc = {'name': 'DC'}
        db.teams.insert_many([marvel, dc])

        # Users (super heroes)
        users = [
            {'name': 'Tony Stark', 'email': 'tony@marvel.com', 'team': 'Marvel'},
            {'name': 'Steve Rogers', 'email': 'steve@marvel.com', 'team': 'Marvel'},
            {'name': 'Bruce Wayne', 'email': 'bruce@dc.com', 'team': 'DC'},
            {'name': 'Clark Kent', 'email': 'clark@dc.com', 'team': 'DC'},
        ]
        db.users.insert_many(users)

        # Activities
        activities = [
            {'user': 'Tony Stark', 'type': 'Run', 'duration': 30},
            {'user': 'Steve Rogers', 'type': 'Swim', 'duration': 45},
            {'user': 'Bruce Wayne', 'type': 'Cycle', 'duration': 60},
            {'user': 'Clark Kent', 'type': 'Fly', 'duration': 120},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'team': 'Marvel', 'points': 150},
            {'team': 'DC', 'points': 180},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'name': 'HIIT', 'difficulty': 'Hard'},
            {'name': 'Yoga', 'difficulty': 'Easy'},
            {'name': 'Strength', 'difficulty': 'Medium'},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data!'))
