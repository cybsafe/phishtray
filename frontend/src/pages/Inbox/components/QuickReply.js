import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Button from '../../../components/Button/ReplyButton';
import { logAction, selectWebpageType } from '../../../utils';
import actionTypes from '../../../config/actionTypes';
import { showWebpage } from '../../../actions/uiActions';

type Props = {
  replies: Array<*>,
  logActionParams: Object,
  setSelectedReplyParams: Object,
  setSelectedReply: () => void,
};

const QuickReply = ({
  replies,
  logActionParams,
  setSelectedReply,
  setSelectedReplyParams,
}: Props) => {
  const { participantId, startTime, emailId } = logActionParams;
  const { activeThread, threads } = useSelector(state => state.exercise);
  const active = threads.filter(thread => thread.id === activeThread);
  const dispatch = useDispatch();

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
            webPage => dispatch(showWebpage(webPage)),
            actionTypes.emailQuickReply
          );
      }}
    />
  ));
};

export default QuickReply;
