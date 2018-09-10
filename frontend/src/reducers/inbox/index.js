// @flow
import { createSelector } from 'reselect';
import produce from 'immer';

import { getAllEmails } from '../../data/threads';
import { getExerciseTimer, getElapsedTime } from '../exercise';

type Email = {
  id: string,
  subject: string,
  from: any, // TODO
  timestamp: Date,
  body: string,
};

type Thread = {
  id: string,
  subject: string,
  from: string, // TODO
  revealTime: number,
  emails: [Email],
};

type State = {
  lastRefreshed: ?Date,
  threads: [Thread],
};

const INITIAL_STATE = {
  lastRefreshed: null,
  threads: [],
};

export default function reducer(state: State = INITIAL_STATE, action = {}) {
  switch (action.type) {
    case 'inbox/LOAD_THREADS': {
      return {
        ...state,
        lastRefreshed: new Date(),
        threads: action.payload,
      };
    }

    case 'inbox/MARK_THREAD_AS_READ': {
      return produce(state, draft => {
        const { threadId } = action.payload;
        const thread = draft.threads.find(thread => thread.id === threadId);
        thread.isRead = true;
      });
    }

    default: {
      return state;
    }
  }
}

// Actions
export function loadThreads() {
  return async dispatch => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    const threads = getAllEmails();

    return dispatch({
      type: 'inbox/LOAD_THREADS',
      payload: threads,
    });
  };
}

// Actions
// Gateway URL:
const API_GATEWAY = 'http://localhost:8282';

export function postUserActions(time, thread, type) {
  const body = {
    milliseconds: time,
    action: {
      type: type,
      associations: [{ exerciseEmail: '345' }, { exerciseEmailReply: '3476' }],
    },
  };

  return async () => {
    const response = await fetch(
      `${API_GATEWAY}/exercise/${thread.id}/actions`,
      {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      }
    );
    const json = await response.json();
    console.log(`POST >> ${type}`, json);
    return {
      type: 'inbox/USER_ACTION',
      payload: {
        json,
      },
    };
  };
}

export function markThreadAsRead(threadId) {
  return {
    type: 'inbox/MARK_THREAD_AS_READ',
    payload: {
      threadId,
    },
  };
}

// Selectors
const inboxSelector = state => state.inbox;
export const getThreads = createSelector(
  [inboxSelector, getExerciseTimer],
  (inbox, exerciseTimer) =>
    inbox.threads.filter(thread => thread.revealTime <= exerciseTimer)
);

export const getThread = createSelector(
  [inboxSelector, (_, props) => props.threadId, getExerciseTimer],
  (inbox, threadId, exerciseTimer) =>
    inbox.threads.find(
      thread => thread.id === threadId && thread.revealTime <= exerciseTimer
    )
);

export const getLastRefreshed = createSelector(
  inboxSelector,
  inbox => inbox.lastRefreshed
);
