import React, { useEffect, useState } from 'react'
import { useParams } from "react-router-dom";
import { ExerciseRealization, getWorkout } from '../../services/Workouts';
import { HttpStatusCode } from 'axios';

export default function ViewWorkout() {

    const { workoutId } = useParams() as { workoutId: string };

    const [title, setTitle] = useState<string>('');
    const [routine, setRoutine] = useState<string>('');
    const [exercises, setExercises] = useState<ExerciseRealization[]>([]);

    useEffect(() => {
        getWorkout(workoutId).then(workout => {
            setTitle(workout.name);
            setRoutine(workout.routine);
            setExercises(workout.exercises);
        }).catch(err => {
            console.log(err.message)
            if (err.response?.status == HttpStatusCode.NotFound){
                alert("Workout not found")      
            }
        })
    }, []);
    
   
    
    return (
        <div>
            <p>Title of workout: {title}</p>
            <p>id: {workoutId}</p>
            <p>Routine: {routine}</p>
            <p>Exercises:</p>
            <ul>
                {exercises.map((exercise) => 
                    <li key={exercise.id}> {exercise.name} {exercise.body_part} {exercise.note}
                        <ul>{exercise.sets.map((set) => <li key={set.order}>{set.reps} {set.weight_kg} {set.rest_sec} </li>)}</ul>
                    </li>)}
            </ul>
        </div>
    )
}
