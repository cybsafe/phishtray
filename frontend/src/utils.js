// @flow

export const fetchAndDispatch = (apiUrl: string, dispatchType: string) => (
  dispatch: *
) =>
  fetch(`http://localhost:9000${apiUrl}`, {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': 'http://localhost:3000',
    },
  })
    .then(response => response.json())
    .then(json =>
      dispatch({
        type: dispatchType,
        payload: json,
      })
    )
    .catch(e => console.error(`Failed to fetch data for ${dispatchType}`));

export const logAction = async actionData => {
  const { participantId, ...rest } = actionData;

  const url = `/api/v1/participants/${participantId}/action/`;

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
    const resJSON = await rawResponse().json();
  } catch (e) {
    console.error('logAction failed', e);
  }
};
