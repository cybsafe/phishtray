// @flow
import { createSelector } from 'reselect';
import { createAction } from '../../api/exercise';

const INITIAL_STATE = {};
const MARK_EMAIL_AS_OPENED = 'email/MARK_EMAIL_AS_OPENED';

export default function reducer(state = INITIAL_STATE, action = {}) {
  switch (action.type) {
    case MARK_EMAIL_AS_OPENED: {
      return {
        ...state,
        opened: {
          [action.payload]: true,
        },
      };
    }

    default: {
      return state;
    }
  }
}

// Actions
export function markEmailAsOpened({ id }) {
  return async (dispatch, getState) => {
    const { timer } = getState().exercise;
    const associations = { exerciseEmail: id };
    await createAction('email_open', associations, timer * 1000);
    dispatch({
      type: MARK_EMAIL_AS_OPENED,
      payload: id,
    });
  };
}

// Selectors
const exerciseSelector = state => state.exercise;

export const getExerciseTimer = createSelector(
  exerciseSelector,
  exercise => exercise.timer
);
