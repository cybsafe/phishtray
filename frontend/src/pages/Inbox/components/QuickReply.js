// @flow
import React from 'react';

import Button from '../../../components/Button/ReplyButton';

import { logAction } from '../../../utils';
import actionTypes from '../../../config/actionTypes';

type Props = {
  replies: Array<*>,
  onClickParams: *,
};

const QuickReply = ({ replies, onClickParams }: Props) => {
  const { participantId, startTime, emailId } = onClickParams;
  return replies.map(reply => (
    <Button
      key={reply.id}
      type={reply.type}
      content={reply.message}
      onClick={() =>
        logAction({
          actionType: actionTypes.emailQuickReply,
          participantId: participantId,
          timeDelta: Date.now() - startTime,
          emailId: emailId,
          replyId: reply.id,
          message: reply.message,
          timestamp: new Date(),
        })
      }
    />
  ));
};

export default QuickReply;
