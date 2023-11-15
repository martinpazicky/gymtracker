# setup_test_data.py
import random

from django.db import transaction
from django.core.management.base import BaseCommand

from apps.core.factories.factory import AccountFactory, ExerciseFactory, UserFactory
from apps.core.models import ExerciseRealization, ExerciseSet, User, Workout, Exercise
from apps.accounts.models import Account


NUM_USERS = 50
NUM_CLUBS = 10
NUM_THREADS = 12
COMMENTS_PER_THREAD = 25
USERS_PER_CLUB = 8

class Command(BaseCommand):
    help = "Generates test data"

   
    @transaction.atomic
    def handle(self, *args, **kwargs):
        models = [Workout, Exercise, ExerciseRealization]
        for m in models:
            m.objects.all().delete()
        self.stdout.write("generating data")
            
        #user = UserFactory()
        #user.account.password = "password"
        # user.account.save()
        acc = Account.objects.create_user('admin@gmail.com', password='admin')
        acc.is_superuser = True
        acc.is_staff = True
        acc.save()
        acc = Account.objects.create_user('user@gmail.com', password='user')
        acc.is_superuser = False
        acc.is_staff = False
        acc.save()
        
        user = User(account=acc, id_number="2")
        user.save()

         # exercise = ExerciseFactory()
        exercise = Exercise(body_part="chest", name="bench press")
        exercise.save()
        exercise2 = Exercise(body_part="chest", name="DB bench press")
        exercise2.save()
        workout = Workout(user_id=user.id)
        workout.save()
        workout = Workout(user_id=user.id,
                          name="druhy workout")
        workout.save()
        exercise_realization = ExerciseRealization.objects.create(
            exercise=exercise,
            workout=workout,
            note="Felt hard"
        )
        exset = ExerciseSet(reps=10, weight_kg=100, rest_sec=60, exercise_realization=exercise_realization, order=1)
        exset.save()
        exset = ExerciseSet(reps=10, weight_kg=120, rest_sec=60, exercise_realization=exercise_realization, order=2)
        exset.save()
        exercise_realization.save()
        exercise_realization = ExerciseRealization.objects.create(
            exercise=exercise2,
            workout=workout,
        )
        exercise_realization.save()
        # workout.exercises.add(exercise, note="aa")
        # workout.save()

        acc = Account.objects.create_user('userr@gmail.com', password='userr')
        acc.is_superuser = False
        acc.is_staff = False
        acc.save()
        
        user = User(account=acc, id_number="3")
        user.save()

        workout = Workout(user_id=user.id)
        workout.save()

       