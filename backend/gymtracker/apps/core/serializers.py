# uneffective queries when requesting workouts with embeded exercises
from rest_framework import serializers
from apps.core.models import Exercise, ExerciseRealization, ExerciseSet, Workout 


class ExerciseSetSerializer(serializers.ModelSerializer):
    exercise_realization_id = serializers.IntegerField()

    def validate(self, attrs):
        order = attrs.get('order')
        exercise_realization_id = attrs.get('exercise_realization_id')
        # unique order within exercise realization constraint
        if ExerciseSet.objects.filter(order=order, exercise_realization_id=exercise_realization_id).exists():
            raise serializers.ValidationError(
                {"order": "Set within this exercise with this order already exists."}
            )
        return super().validate(attrs)
    
    def to_representation(self, obj):
        ret = super(serializers.ModelSerializer, self).to_representation(obj)
        ret.pop('exercise_realization_id')
        return ret 
    
    class Meta:
        model = ExerciseSet 
        fields = ('id', 'exercise_realization_id', 'reps', 'weight_kg', 'rest_sec', 'order')

        
class ExerciseRealizationSerializer(serializers.ModelSerializer):
    exercise_id = serializers.IntegerField()
    name = serializers.ReadOnlyField(source='exercise.name')
    body_part = serializers.ReadOnlyField(source='exercise.body_part')
    note = serializers.CharField(required=False)
    sets = ExerciseSetSerializer(source='exerciseset_set', many=True, read_only=True)

    def validate(self, attrs):
        if not Exercise.objects.filter(id=attrs['exercise_id']).exists():
            raise serializers.ValidationError(
                {"exercise_id": "Exercise with this id does not exist."}
            )
        return attrs
    
    class Meta:
        model = ExerciseRealization
        fields = ('id', 'exercise_id', 'name', 'body_part', 'note', 'sets')


class ExerciseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Exercise
        fields = 'id', 'name', 'body_part'


class EmbeddedRelationsWorkoutDetailSerializer(serializers.ModelSerializer):
    exercises = ExerciseRealizationSerializer(source='exerciserealization_set', many=True)

    class Meta:
        model = Workout
        fields = '__all__'

class WorkoutDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workout
        fields = ['id', 'date', 'name', 'routine']


class WorkoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workout
        fields = ["id", "date", "name"]
