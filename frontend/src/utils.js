// @flow
import Cookies from 'js-cookie';

export const HOST_BACKEND = process.env.REACT_APP_HOST_BACKEND || process.env.REACT_APP_HOST;
export const HOST_FRONTEND = process.env.REACT_APP_HOST_FRONTEND || process.env.REACT_APP_HOST;

export const fetchAndDispatch = (apiUrl: string, dispatchType: string) => (
  dispatch: *
) =>
  fetch(`${HOST_BACKEND}${apiUrl}`, {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': HOST_FRONTEND,
    },
  })
    .then(response => response.json())
    .then(json =>
      dispatch({
        type: dispatchType,
        payload: json,
      })
    )
    .catch(e => console.error(`Failed to fetch data for ${dispatchType}`, e));

export const logAction = async (actionData: object) => {
  const { participantId, ...rest } = actionData;

  const url = `${HOST_BACKEND}/api/v1/participants/${participantId}/action/`;

  const rawResponse = () =>
    fetch(url, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken'),
      },
      body: JSON.stringify({
        ...rest,
      }),
    });

  try {
    await rawResponse();
  } catch (e) {
    console.error('logAction failed', e);
  }
};

export const postFormData = async (apiUrl: string, data: Object) => {
  const postResponse = () =>
    fetch(`${HOST_BACKEND}${apiUrl}`, {
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': HOST_FRONTEND,
        'X-CSRFToken': Cookies.get('csrftoken'),
      },
      method: 'POST',
      body: JSON.stringify(data),
    });

  try {
    await postResponse();
  } catch (e) {
    console.error('postAction failed', e);
  }
};

export const getHeaderText = location => {
  switch (location) {
    case '/inbox':
      return 'Inbox';
    case '/accounts':
      return 'Accounts';
    case '/files':
      return 'Files';
    case '/web':
      return 'Web';
    case '/staff-profiles':
      return 'Staff Profiles';
    default:
      return location.split('/')[1] || 'Inbox';
  }
};

export const getRange = (start, end) =>
  Array(end - start + 1)
    .fill()
    .map((_, idx) => start + idx);
