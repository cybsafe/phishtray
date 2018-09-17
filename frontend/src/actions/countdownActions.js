//@flow

export const startCountdown = (minutes: number) => async (dispatch: *) => {
  console.log('START COUNTDOWN');
  dispatch({
    type: 'countdown/SET_TIME',
    payload: {
      startTime: Date.now(),
      countdownMins: minutes,
    },
  });
};
