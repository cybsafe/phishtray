type CountdownState = {
  startTime: number,
  countdownSecs: number,
};

const INITIAL_STATE = {
  startTime: 0, // Date.now(),
  countdownMins: 0, // 25,
};

const reducer = (state: CountdownState = INITIAL_STATE, action = {}) => {
  switch (action.type) {
    case 'countdown/SET_TIME':
      return {
        ...state,
        startTime: action.payload.startTime,
        countdownMins: action.payload.countdownMins,
      };
    default:
      return state;
  }
};

export default reducer;
