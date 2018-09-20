// @flow
import { createSelector } from 'reselect';
import { fetchAndDispatch } from '../../utils';
import produce from 'immer';

const INITIAL_STATE = {
  timer: 0, // exercise time elapsed in seconds
  startTime: 0, // Date.now() when form submitted,
};

export default function reducer(state = INITIAL_STATE, action = {}) {
  switch (action.type) {
    case 'exercise/TIMER_TICK': {
      return produce(state, draft => {
        draft.timer += action.payload.amount;
      });
    }

    case 'exercise/LOAD_DATA': {
      return {
        ...state,
        ...action.payload.exercise,
        lastRefreshed: new Date(),
      };
    }

    case 'exercise/MARK_THREAD_AS_READ': {
      return produce(state, draft => {
        const { threadId } = action.payload;
        const thread = draft.threads.find(thread => thread.id === threadId);
        thread.isRead = true;
      });
    }

    case 'exercise/SET_START_TIME':
      return {
        ...state,
        startTime: action.payload.startTime,
      };

    default:
      return state;
  }
}

// Actions TODO: move exercise actions to /actions/exerciseActions

export function tickTimer(amount = 10) {
  return {
    type: 'exercise/TIMER_TICK',
    payload: {
      amount,
    },
  };
}

export function markThreadAsRead(threadId) {
  return {
    type: 'exercise/MARK_THREAD_AS_READ',
    payload: {
      threadId,
    },
  };
}

export const getExerciseData = (exerciseUuid: string) =>
  fetchAndDispatch(
    `/api/v1/exercises/${exerciseUuid}/init`,
    'exercise/LOAD_DATA'
  );

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

export const getThreads = createSelector(exerciseSelector, exercise =>
  exercise.threads.filter(
    thread =>
      exercise.emailRevealTimes.filter(time => time.emailId === thread.id)[0]
        .revealTime <= exercise.timer
  )
);

export const getThread = createSelector(
  [exerciseSelector, (_, props) => props.threadId, getExerciseTimer],
  (exercise, threadId) =>
    exercise.threads.find(
      thread =>
        thread.id === threadId &&
        exercise.emailRevealTimes.filter(time => time.emailId === thread.id)[0]
          .revealTime <= exercise.timer
    )
);
