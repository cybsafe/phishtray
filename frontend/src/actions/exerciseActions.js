//@flow
import { fetchAndDispatch } from '../utils';

export const startCountdown = () => async (dispatch: *) => {
  dispatch({
    type: 'exercise/SET_START_TIME',
    payload: {
      startTime: Date.now(),
    },
  });
};

export function tickTimer(amount: number = 10) {
  return {
    type: 'exercise/TIMER_TICK',
    payload: {
      amount,
    },
  };
}

export function markThreadAsRead(threadId: string) {
  return {
    type: 'exercise/MARK_THREAD_AS_READ',
    payload: {
      threadId,
    },
  };
}

export function markThreadAsDeleted(threadId: string) {
  return {
    type: 'exercise/MARK_THREAD_AS_DELETED',
    payload: {
      threadId,
    },
  };
}

export function markThreadAsActive(threadId: string) {
  return {
    type: 'exercise/MARK_THREAD_AS_ACTIVE',
    payload: {
      threadId,
    },
  };
}

export function markThreadAsInactive() {
  return {
    type: 'exercise/MARK_THREAD_AS_INACTIVE',
    payload: {
      threadId: '',
    },
  };
}

export const getExerciseData = (exerciseUuid: string) =>
  fetchAndDispatch(
    `/api/v1/exercises/${exerciseUuid}/init`,
    'exercise/LOAD_DATA'
  );

export function setSelectedReply(params: Object) {
  const { threadId, selectedReplyid, emailid } = params;
  return {
    type: 'exercise/SET_SELECTED_REPLY',
    payload: {
      threadId,
      selectedReplyid,
      emailid,
    },
  };
}
