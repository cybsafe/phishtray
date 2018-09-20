//@flow

export const startCountdown = () => async (dispatch: *) => {
  dispatch({
    type: 'exercise/SET_START_TIME',
    payload: {
      startTime: Date.now(),
    },
  });
};
