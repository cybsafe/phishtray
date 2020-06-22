// @flow
import produce from 'immer';
import type { ExerciseState } from '../types/exerciseTypes';

const INITIAL_STATE: ExerciseState = {
  timer: 0, // exercise time elapsed in seconds
  startTime: 0, // Date.now() when form submitted,
  threads: [],
  activeThread: '',
  inlineNotification: null,
  participant: null,
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

    case 'exercise/CLEAR_PARTICIPANT_ID': {
      return {
        ...state,
        participant: null,
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

    case 'exercise/MARK_THREAD_AS_DELETED': {
      return {
        ...state,
        threads: state.threads.filter(
          thread => thread.id !== action.payload.threadId
        ),
      };
    }

    case 'exercise/SET_START_TIME':
      return {
        ...state,
        startTime: action.payload.startTime,
      };

    case 'exercise/RESET_COUNTDOWN':
      return {
        ...state,
        startTime: action.payload.startTime,
        timer: action.payload.timer,
      };

    case 'exercise/SET_SELECTED_REPLY':
      return produce(state, draft => {
        const { threadId, selectedReplyid, emailid } = action.payload;
        const thread = draft.threads.find(thread => thread.id === threadId);
        const email = thread.emails.find(email => email.id === emailid);
        email.replies = email.replies.filter(
          reply => reply.id === selectedReplyid
        );
        email.isReplied = true;
      });

    case 'exercise/MARK_THREAD_AS_ACTIVE':
      return {
        ...state,
        activeThread: action.payload.threadId,
      };

    case 'exercise/MARK_THREAD_AS_INACTIVE':
      return {
        ...state,
        activeThread: action.payload.threadId,
      };

    case 'exercise/SET_INLINE_NOTIFICATION':
      return {
        ...state,
        inlineNotification: action.payload.term,
      };

    case 'exercise/UNSET_INLINE_NOTIFICATION':
      return {
        ...state,
        inlineNotification: null,
      };

    default:
      return state;
  }
}
