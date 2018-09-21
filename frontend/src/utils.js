// @flow

const HOST_BACKEND = 'http://phishtray.local:9000';
const HOST_FRONTEND = 'http://phishtray.local:3000';

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

export const logAction = async (actionData: *) => {
  const { participantId, ...rest } = actionData;

  const url = `${HOST_BACKEND}/api/v1/participants/${participantId}/action/`;

  const rawResponse = () =>
    fetch(url, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...rest,
      }),
    });

  try {
    const res = await rawResponse();
  } catch (e) {
    console.error('logAction failed', e);
  }
};

export const postFormData = (apiUrl: string, data: Object) => {
  fetch(`${HOST_BACKEND}${apiUrl}`, {
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': HOST_FRONTEND,
    },
    method: 'POST',
    body: JSON.stringify(data),
  })
    .then(response => console.log(response.json()))
    .catch(e => console.error('Failed to post form data', e));
};
