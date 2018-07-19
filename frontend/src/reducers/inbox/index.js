// @flow
import { createSelector } from 'reselect';

import { getAllEmails } from '../../data/threads';

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
  emails: [Email],
};

type State = {
  lastRefreshed: ?Date,
  threads: [Thread],
};

const INITIAL_STATE = {
  lastRefreshed: null,
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
export const getThreads = createSelector(inboxSelector, inbox => inbox.threads);

export const getThread = createSelector(
  [inboxSelector, (_, props) => props.threadId],
  (inbox, threadId) => inbox.threads.find(thread => thread.id === threadId)
);

export const getLastRefreshed = createSelector(
  inboxSelector,
  inbox => inbox.lastRefreshed
);
