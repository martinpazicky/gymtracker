import React, { useEffect, useState } from 'react'
import { ExerciseDefinition, getExerciseDefinitions } from '../../services/ExerciseDefinitions';
import { HttpStatusCode } from 'axios';
import Collapsible from 'react-collapsible';

export default function ViewExercises() {

    const [allExerciseDefinitions, setAllExerciseDefinitions] = useState<ExerciseDefinition[]>([]);
    const [filteredList, setFilteredList] = useState<ExerciseDefinition[]>([]);
    
    useEffect(() => {
        getExerciseDefinitions().then(exerciseDefinitions => {
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
            return item.name.toLowerCase().indexOf(query.toLowerCase()) !== -1;
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
                <li key={exerciseDefinition.id}>{exerciseDefinition.name}
                    <Collapsible trigger="View details >">
                    <ul>
                        <li>1RM: </li>
                        <li>Best set: </li>
                    </ul>
                    </Collapsible>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )
}
