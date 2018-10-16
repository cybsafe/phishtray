// @flow
import produce from 'immer';

import websites from '../components/WebBrowser/websites';

// eslint-disable-next-line no-undef
type WebPage = $Keys<typeof websites>;

type State = {
  webBrowser: ?{
    page: WebPage,
    emailId: String,
  },
};

const INITIAL_STATE = {
  webBrowser: null,
};

export default function reducer(
  state: State = INITIAL_STATE,
  action: Object = {}
) {
  switch (action.type) {
    case 'ui/VIEW_WEBPAGE': {
      return produce(state, draft => {
        draft.webBrowser = {
          page: action.payload,
          emailId: action.emailId,
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
