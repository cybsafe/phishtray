//@flow

export const startCountdown = (minutes: number) => async (dispatch: *) => {
  dispatch({
    type: 'countdown/SET_TIME',
    payload: {
      startTime: Date.now(),
      countdownMins: minutes,
    },
  });
};
