// @flow
import { createSelector } from 'reselect';
import { fetchAndDispatch } from '../../utils';

const INITIAL_STATE = {
  timer: 0, // exercise time elapsed in seconds
};

export default function reducer(state = INITIAL_STATE, action = {}) {
  switch (action.type) {
    case 'exercise/TIMER_TICK':
      return {
        ...state,
        timer: (state.timer += action.payload.amount),
      };

    case 'exercise/LOAD_DATA':
      return {
        ...state,
        ...action.payload,
        lastRefreshed: new Date(),
      };

    default:
      return state;
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

export const getExerciseData = (exerciseUuid: string) =>
  fetchAndDispatch(`/api/v1/exercises/${exerciseUuid}/`, 'exercise/LOAD_DATA');

// Selectors
const exerciseSelector = state => state.exercise;

export const getLastRefreshed = createSelector(
  exerciseSelector,
  exercise => exercise.lastRefreshed
);

export const getExercise = createSelector(
  exerciseSelector,
  exercise => exercise
);

export const getExerciseTimer = createSelector(
  exerciseSelector,
  exercise => exercise.timer
);
