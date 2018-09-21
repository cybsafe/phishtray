import { createSelector } from 'reselect';

import websites from '../components/WebBrowser/websites';

const uiSelector = state => state.ui;

export const getWebpage = createSelector(
  [uiSelector],
  ui => (ui.webBrowser ? websites[ui.webBrowser.page] : null)
);
