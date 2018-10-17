// @flow
import React from 'react';

import Button from '../../../components/Button/ReplyButton';

import { logAction } from '../../../utils';
import actionTypes from '../../../config/actionTypes';

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
      }}
    />
  ));
};

export default QuickReply;
