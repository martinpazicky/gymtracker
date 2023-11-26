
import React, { useState } from 'react';
import { ExerciseDefinition } from '../../../services/ExerciseDefinitions';
// https://contactmentor.com/build-reactjs-search-filter/

type ExerciseDefinitionsListProps = {
  data: ExerciseDefinition[]
  onAddExercise: (idToAdd: number) => void
}

export default function ExerciseDefinitionsList(props: ExerciseDefinitionsListProps) {

    const itemList = props.data
    
    const [filteredList, setFilteredList] = useState(itemList);

    const filterBySearch = (event: React.ChangeEvent<HTMLInputElement>) => {
        const query = event.target.value;
        let updatedList = [...itemList];
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
                  <button onClick={( )=> props.onAddExercise(exerciseDefinition.id)}>+</button>
                </li>
              ))}
            </ul>
          </div>
        </div>
      );
}