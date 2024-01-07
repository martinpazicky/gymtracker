import React, { useState } from "react";
import { ExerciseSet, addSet } from "../../services/Workouts";
import ExerciseSetComponent from "./ExerciseSet";

type ExerciseSetListProps = {
    sets: ExerciseSet[];
    exerciseId: number;
}

const ExerciseSetListComponent: React.FC<ExerciseSetListProps> = (props: ExerciseSetListProps) => {
    const [edit, setEdit] = useState(false);
    const [exerciseSets, setExerciseSets] = useState<ExerciseSet[]>(props.sets);

    async function handleAdd() {
        const newSet = { order: exerciseSets.length + 1, reps: 0, weight_kg: 0, rest_sec: 0 };
        await addSet(
            props.exerciseId,
            newSet
        ).then(({data, status})=> {
            const newList = exerciseSets.concat(data);
            console.log(newList)    
            setExerciseSets(newList);
        }).catch(err => {alert(err)});
    }

    return (
        <div>
            <ul>
                {exerciseSets.map((set) => 
                <li key={set.order}>
                    <ExerciseSetComponent key={set.order} exerciseId={props.exerciseId} set={set} edit={true}></ExerciseSetComponent>
                </li>)}
            </ul>
            <button type="button" onClick={handleAdd}>
            +
            </button>
        </div>
    );
};

export default ExerciseSetListComponent;