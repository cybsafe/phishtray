// @flow
import { createSelector } from 'reselect';
import produce from 'immer';

import websites from '../../components/WebBrowser/websites';

// eslint-disable-next-line no-undef
type WebPage = $Keys<typeof websites>;

type State = {
  webBrowser: ?{
    page: WebPage,
  },
};

const INITIAL_STATE = {
  webBrowser: null,
};

export default function reducer(state: State = INITIAL_STATE, action = {}) {
  switch (action.type) {
    case 'ui/VIEW_WEBPAGE': {
      return produce(state, draft => {
        draft.webBrowser = {
          page: action.payload,
        };
      });
    }

    case 'ui/CLOSE_WEBPAGE': {
      return produce(state, draft => {
        draft.webBrowser = null;
      });
    }

    default: {
      return state;
    }
  }
}

// Actions
export function showWebpage(webPage: WebPage) {
  return {
    type: 'ui/VIEW_WEBPAGE',
    payload: webPage,
  };
}

export function closeWebpage() {
  return {
    type: 'ui/CLOSE_WEBPAGE',
  };
}

// Selectors
const uiSelector = state => state.ui;
export const getWebpage = createSelector(
  [uiSelector],
  ui => (ui.webBrowser ? websites[ui.webBrowser.page] : null)
);
