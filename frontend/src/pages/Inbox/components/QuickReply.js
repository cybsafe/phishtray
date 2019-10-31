import React from 'react';
import Button from '../../../components/Button/ReplyButton';
import { connect } from 'react-redux';
import { logAction, selectWebpageType } from '../../../utils';
import actionTypes from '../../../config/actionTypes';
import { showWebpage } from '../../../actions/uiActions';

type Props = {
  replies: Array<*>,
  logActionParams: Object,
  setSelectedReplyParams: Object,
  setSelectedReply: () => void,
  activeThread: Number,
  threads: Array<*>,
  showWebpage: () => void,
};

const QuickReply = ({
  replies,
  logActionParams,
  setSelectedReply,
  setSelectedReplyParams,
  activeThread,
  threads,
  showWebpage,
}: Props) => {
  const { participantId, startTime, emailId } = logActionParams;

  const active = threads.filter(thread => thread.id === activeThread);

  const {
    interceptExercise,
    releaseCodes,
    webPage,
  } = active[0].threadProperties;

  return replies.map(reply => (
    <Button
      key={reply.id}
      type={reply.type}
      content={reply.message}
      onClick={() => {
        setSelectedReply({
          selectedReplyid: reply.id,
          ...setSelectedReplyParams,
        });
        logAction({
          actionType: actionTypes.emailQuickReply,
          participantId: participantId,
          timeDelta: Date.now() - startTime,
          emailId: emailId,
          replyId: reply.id,
          message: reply.message,
          timestamp: new Date(),
        });
        webPage &&
          selectWebpageType(
            interceptExercise,
            releaseCodes,
            showWebpage,
            actionTypes.emailQuickReply
          );
      }}
    />
  ));
};

export default connect(
  state => ({
    activeThread: state.exercise.activeThread,
    threads: state.exercise.threads,
    exercise: state.exercise,
  }),
  { showWebpage }
)(QuickReply);
