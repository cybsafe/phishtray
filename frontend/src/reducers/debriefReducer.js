const INITIAL_STATE = {
  phishingEmails: [],
  scores: [],
};

export default function reducer(state: INITIAL_STATE, action: {}) {
  switch (action.type) {
    case 'debrief/LOAD_DATA': {
      return {
        ...state,
        ...action.payload,
        phishingEmails: action.payload.phishingEmails,
        scores: action.payload.scores,
      };
    }

    default:
      return INITIAL_STATE;
  }
}
