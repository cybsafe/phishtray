// @flow
import { createSelector } from 'reselect';
import produce from 'immer';

import { getAllEmails } from '../data/threads';
import { getExerciseTimer } from '../selectors/exerciseSelectors';

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
  fromAccount: string, // TODO
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
