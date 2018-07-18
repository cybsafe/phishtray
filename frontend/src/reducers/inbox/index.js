// @flow

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
export function getThreads(state) {
  return state.inbox.threads;
}

export function getThread(id) {
  return state => state.inbox.threads.find(thread => thread.id === id);
}

export function getLastRefreshed(state) {
  return state.inbox.lastRefreshed;
}
