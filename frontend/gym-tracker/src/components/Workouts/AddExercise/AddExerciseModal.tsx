import React, { useEffect, useState } from 'react';
import ReactModal from 'react-modal';
import Modal from 'react-modal';
import { ExerciseDefinition, getExerciseDefinitions } from '../../../services/ExerciseDefinitions';
import { HttpStatusCode } from 'axios';
import ExerciseDefinitionsList from './ExerciseDefinitionsList';

const customStyles = {
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    width: '70%',
    bottom: 'auto',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)'
  }
};

type AddExerciseProps = {
    IsModalOpened: boolean
    onCloseModal: () => void
    onAddExercise: (idToAdd: number) => void
}

export default function AddExerciseModalComponent(props: AddExerciseProps) {

    function onModalClose() {
        props.onCloseModal();
    }

    function onAddExercise(idToAdd: number) {
        if (idToAdd == undefined)
            return;
        props.onAddExercise(idToAdd);
    }

    const [exerciseDefinitions, setExerciseDefinitions] = useState<ExerciseDefinition[]>([]);
    useEffect(() => {
        getExerciseDefinitions().then(exerciseDefinitions => {
          setExerciseDefinitions(exerciseDefinitions.data);
        }).catch(err => {
            console.log(err.message)
            if (err.response?.status == HttpStatusCode.NotFound){
                alert("error")      
            }
        })
    }, []);

  return (
    <div>
      <ReactModal
        isOpen={props.IsModalOpened}
        style={customStyles}
        ariaHideApp={false}
        shouldCloseOnOverlayClick={true}
        onRequestClose={onModalClose}
      >
        <h2>Add Exercise</h2>

        <ExerciseDefinitionsList data={exerciseDefinitions} onAddExercise={onAddExercise}/>

        <button onClick={onModalClose}>Done</button>
      </ReactModal>
    </div>
  );
}

