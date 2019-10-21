const INITIAL_STATE = {
  phishingEmails: [],
  scores: [],
  debrief: false,
};

export default function reducer(state: INITIAL_STATE, action: {}) {
  switch (action.type) {
    case 'debrief/LOAD_DATA': {
      return {
        ...state,
        ...action.payload,
        phishingEmails: action.payload.phishingEmails,
        scores: action.payload.scores,
        debrief: action.payload.debrief,
      };
    }

    default:
      return INITIAL_STATE;
  }
}
