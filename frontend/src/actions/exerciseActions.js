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

export const resetCountdown = () => (dispatch: *) => {
  dispatch({
    type: 'exercise/RESET_COUNTDOWN',
    payload: {
      startTime: 0,
      timer: 0,
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

export function clearParticipantId() {
  return {
    type: 'exercise/CLEAR_PARTICIPANT_ID',
  };
}

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

export function setInlineNotification(term: string) {
  return {
    type: 'exercise/SET_INLINE_NOTIFICATION',
    payload: { term },
  };
}

export function unsetInlineNotification() {
  return {
    type: 'exercise/UNSET_INLINE_NOTIFICATION',
  };
}
