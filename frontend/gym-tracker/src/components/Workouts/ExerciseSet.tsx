import debounce from "lodash.debounce";
import { ExerciseSet, ExerciseSetInput, updateSet } from "../../services/Workouts";
import React, { useCallback, useState } from "react";
import exp from "constants";

type ExerciseSetProps = {
    exerciseId: number;
    set: ExerciseSet;
}


const ExerciseSetComponent: React.FC<ExerciseSetProps> = (props: ExerciseSetProps) => {
    const [edit, setEdit] = useState(false);
    const [exerciseSet, setExerciseSet] = useState<ExerciseSet>(props.set);

    function apiCall(set: ExerciseSetInput, setId: number) {
        console.log("calling api")
        updateSet(props.exerciseId, setId, set)
    }

    const debouncedApiCall = useCallback(
        debounce((set: ExerciseSetInput, setId) => apiCall(set, setId), 1000),
        []
    );

    function handleEdit(field: keyof ExerciseSet, event: React.ChangeEvent<HTMLInputElement>, naturalNubersOnly=false){
        let value = event.target.value.replace(/-/g, ''); // remove minus sign
        if (naturalNubersOnly)
            value = event.target.value.replace(/\D/g, ''); // remove non digits
        if (value === '') return;

        event.target.value = value;
        const updatedSet = { ...exerciseSet, [field]: Number(value)};
        setExerciseSet(updatedSet);
        const { id, ...updatedSetInput } = updatedSet; // remove id
        debouncedApiCall(updatedSetInput, updatedSet.id)
    }

    return (
        <div>
            <input
                type="number"
                defaultValue={exerciseSet.reps}
                onChange={(e) => handleEdit('reps', e, true)}
            />
             <input
                type="number"
                defaultValue={exerciseSet.weight_kg}
                onChange={(e) => handleEdit('weight_kg', e)}
            />
             <input
                type="number"
                defaultValue={exerciseSet.rest_sec}
                onChange={(e) => handleEdit('rest_sec', e)}
            />
        </div>
    );
};

export default ExerciseSetComponent;