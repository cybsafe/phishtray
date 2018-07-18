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
  threads: [Thread],
};

export default function reducer(state: State = {}, action = {}) {
  switch (action.type) {
    case 'inbox/LOAD_THREADS': {
      return {
        ...state,
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
  return state.threads;
}

export function getThread(id) {
  return state => state.threads.find(thread => thread.id === id);
}
