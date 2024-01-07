import React, { useEffect, useState } from 'react'
import { HttpStatusCode } from 'axios';
import Collapsible from 'react-collapsible';
import ExerciseSetComponent from '../Workouts/ExerciseSet';
import { ExercisePersonalRecord, getExercisePersonalRecords } from '../../services/PersonalRecords';
import { ExerciseSet } from '../../services/Workouts';

export default function ViewExercises() {

    const [allExerciseDefinitions, setAllExerciseDefinitions] = useState<ExercisePersonalRecord[]>([]);
    const [filteredList, setFilteredList] = useState<ExercisePersonalRecord[]>([]);
    
    useEffect(() => {
        getExercisePersonalRecords().then(exerciseDefinitions => {
          setAllExerciseDefinitions(exerciseDefinitions.data);
          setFilteredList(exerciseDefinitions.data);
        }).catch(err => {
            console.log(err.message)
            if (err.response?.status == HttpStatusCode.NotFound){
                alert("error")      
            }
        })
    }, []);

    const filterBySearch = (event: React.ChangeEvent<HTMLInputElement>) => {
        const query = event.target.value;
        let updatedList = [...allExerciseDefinitions];
        // Include all elements which includes the search query
        // this part can be replaced with api call
        updatedList = updatedList.filter((item) => {
            return item.exercise_name.toLowerCase().indexOf(query.toLowerCase()) !== -1;
        });
        // Trigger render with updated values
        setFilteredList(updatedList);
    };

    return (
        <div>
          <div className="search-header">
            <div className="search-text">Search:</div>
            <input id="search-box" onChange={filterBySearch} />
          </div>
          <div id="item-list">
            <ul>
              {filteredList.map((exerciseDefinition) => (
                <li key={exerciseDefinition.exercise_id}>{exerciseDefinition.exercise_name}
                    <Collapsible trigger="View details >">
                    <ul>
                        <li>Best set: {exerciseDefinition.best_set ?
                         (<ExerciseSetComponent exerciseId={exerciseDefinition.exercise_id} set={exerciseDefinition.best_set} edit={false}/>)
                          : "This exercise haven't been performed yet."}
                         </li>
                    </ul>
                    </Collapsible>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )
}
