// @flow
import produce from 'immer';
import type {
  FormQuestion,
  ExerciseThread,
  EmailRevealTime,
} from '../types/exerciseTypes';

type ExerciseState = {
  timer: number,
  startTime: number,
  // from API
  id?: string,
  title?: string,
  description?: string,
  introduction?: string,
  afterword?: string,
  lengthMinutes?: number,
  profileForm?: FormQuestion[],
  threads: ExerciseThread[],
  emailRevealTimes?: EmailRevealTime[],
  participant?: string,
  lastRefreshed?: string,
};

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
        /* eslint-disable-next-line */
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
