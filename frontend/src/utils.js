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
