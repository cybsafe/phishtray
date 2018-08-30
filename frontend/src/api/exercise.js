export const createAction = (actionType, associations, milliseconds) =>
  fetch('/exercise/1/action/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      milliseconds,
      action: {
        type: actionType,
        associations,
      },
    }),
  });
