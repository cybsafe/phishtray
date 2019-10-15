import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { getDebriefData as getDebrief } from '../../actions/debriefActions';

function Debrief({
  match: {
    params: { participantUuid },
  },
  getDebrief,
}) {
  useEffect(() => {
    getDebrief(participantUuid);
  }, [participantUuid]);

  return (
    <div>
      <div>Debrief</div>
    </div>
  );
}

export default connect(
  state => ({
    phishingEmails: state.debrief.phishingEmails,
    scores: state.debrief.scores,
  }),
  { getDebrief }
)(Debrief);
