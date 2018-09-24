// @flow
import produce from 'immer';
import type { ExerciseState } from '../types/exerciseTypes';

const INITIAL_STATE: ExerciseState = {
  timer: 0, // exercise time elapsed in seconds
  startTime: 0, // Date.now() when form submitted,
  threads: [],
};

export default function reducer(
  state: ExerciseState = INITIAL_STATE,
  action: Object = {}
) {
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
        participant: action.payload.participant,
        lastRefreshed: new Date(),
      };
    }

    case 'exercise/MARK_THREAD_AS_READ': {
      return produce(state, draft => {
        const { threadId } = action.payload;
        const thread = draft.threads.find(thread => thread.id === threadId);
        const isRead = thread && true;
        thread.isRead = isRead;
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
