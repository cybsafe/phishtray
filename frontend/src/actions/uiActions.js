// @flow
import websites from '../components/WebBrowser/websites';

// eslint-disable-next-line no-undef
type WebPage = $Keys<typeof websites>;

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
