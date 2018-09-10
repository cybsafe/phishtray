// @flow
import { createSelector } from 'reselect';

const INITIAL_STATE = {
  timer: 0, // exercise time elapsed in seconds
  startTime: new Date(),
};

export default function reducer(state = INITIAL_STATE, action = {}) {
  switch (action.type) {
    case 'exercise/TIMER_TICK': {
      return {
        ...state,
        timer: (state.timer += action.payload.amount),
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

// Selectors
const exerciseSelector = state => state.exercise;

export const getExerciseTimer = createSelector(
  exerciseSelector,
  exercise => exercise.timer
);

const timeSelector = state => state.exercise;

export const getElapsedTime = createSelector(timeSelector, exercise => {
  return new Date() - exercise.startTime;
});
