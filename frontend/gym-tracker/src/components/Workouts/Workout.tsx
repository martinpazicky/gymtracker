import React, { useEffect, useState } from 'react'
import { Link, useParams } from "react-router-dom";
import { ExerciseRealization, addExercise, getWorkout } from '../../services/Workouts';
import { HttpStatusCode } from 'axios';
import ExerciseSetListComponent from './ExerciseSetList';

import ReactModal from 'react-modal';
import AddExerciseModalComponent from './AddExercise/AddExerciseModal';
import Paths from '../../routes/Paths';



export default function ViewWorkout() {
    const { workoutId } = useParams() as { workoutId: string };
    console.log(workoutId)
    const [title, setTitle] = useState<string>('');
    const [routine, setRoutine] = useState<string>('');
    const [exercises, setExercises] = useState<ExerciseRealization[]>([]);

    const [showModal, setShowModal] = useState(false);
   
    function handleOpenModal () {
        setShowModal(true);
    }

    function handleCloseModal() {
        setShowModal(false);
    }

    function handleAddExercise(idToAdd: number) {
        addExercise(Number(workoutId), idToAdd).then(({data, status})=> {
            if (status == HttpStatusCode.Created){
                exercises.push(data);
                setExercises(exercises);
            }
            else
                alert("Something went wrong")
        }).catch(err => {alert(err)});
    }


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
    }, [workoutId]);
    
    
    return (
        <div>
            <p>Title of workout: {title}</p>
            <p>id: {workoutId}</p>
            <p>Routine: {routine}</p>
            <p>Exercises:</p>
            <ul>
                {exercises.map((exercise) => 
                <li key={exercise.id}> {exercise.name} {exercise.body_part} {exercise.note}
                 {exercise.previous_workout_id ? <Link to={Paths.WORKOUTS + (exercise.previous_workout_id)}> Previous performance </Link> : ""}
                    <ExerciseSetListComponent key={0} exerciseId={exercise.id} sets={exercise.sets}></ExerciseSetListComponent>
                </li>)}
            </ul>

            <button onClick={handleOpenModal}>Add Exercise</button>
            <AddExerciseModalComponent 
                IsModalOpened={showModal}
                onCloseModal={handleCloseModal}
                onAddExercise={handleAddExercise}
            />
        </div>
    )
}
