// @flow
import { createSelector } from 'reselect';
import { loadExercise } from '../../data/exercises';

const INITIAL_STATE = {
  timer: 0, // exercise time elapsed in seconds
  lastRefreshed: null,
  exerciseContent: [],
};

export default function reducer(state = INITIAL_STATE, action = {}) {
  switch (action.type) {
    case 'exercise/TIMER_TICK': {
      return {
        ...state,
        timer: (state.timer += action.payload.amount),
      };
    }

    case 'exercise/LOAD_EXERCISE': {
      return {
        ...state,
        lastRefreshed: new Date(),
        exerciseContent: action.payload,
      };
    }

    default: {
      return state;
    }
  }
}

// Actions

export function tickTimer(amount = 10) {
  return {
    type: 'exercise/TIMER_TICK',
    payload: {
      amount,
    },
  };
}

export function loadExercises() {
  return async dispatch => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    const exercise = loadExercise();
    return dispatch({
      type: 'exercise/LOAD_EXERCISE',
      payload: exercise,
    });
  };
}

// Selectors
const exerciseSelector = state => state.exercise;

export const getLastRefreshed = createSelector(
  exerciseSelector,
  exercise => exercise.lastRefreshed
);

export const getExercise = createSelector(
  exerciseSelector,
  exercise => exercise.exerciseContent
);

export const getExerciseTimer = createSelector(
  exerciseSelector,
  exercise => exercise.timer
);
