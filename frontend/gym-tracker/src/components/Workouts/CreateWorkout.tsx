import React, { useState } from 'react'
import { createWorkout } from '../../services/Workouts';

export default function CreateWorkout() {
    const [title, setTitle] = useState('');
    const [routine, setRoutine] = useState('');

    const handleCreatePost = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        await createWorkout(
            {
                name: title, 
                routine: routine
            }
        ).then(({data, status})=> {
            if (status === 201){
                alert("Workout created")
            }else{  
                alert("Something went wrong")
            }
        }).catch(err => {alert(err)});
    }
    
    return (
        <form onSubmit={handleCreatePost}>
            <label>
            <p>Title of workout</p>
            <input type="text" onChange={e => setTitle(e.target.value)} />
            </label>
            <label>
            <p>Routine</p>
            <input type="text" onChange={e => setRoutine(e.target.value)} />
            </label>
            <div>
             <button type="submit">Submit</button>
            </div>
        </form>
    )
}
