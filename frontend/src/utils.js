// @flow

export const fetchAndDispatch = (apiUrl: string, dispatchType: string) => (
  dispatch: *
) =>
  fetch(`http://phishtray.local:9000${apiUrl}`, {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': 'http://phishtray.local:3000',
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

export const logAction = async actionData => {
  const { participantId, ...rest } = actionData;

  console.log('logAction actionData', actionData);

  const url = `http://phishtray.local:9000/api/v1/participants/${participantId}/action/`;

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
