import { fetchAndDispatch } from '../utils';

export const getDebriefData = (participantUuid: string) => {
  fetchAndDispatch(
    `/api/v1/participant-scores/${participantUuid}`,
    'debrief/LOAD_DATA'
  );
};
