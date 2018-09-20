import React from 'react';

import Button from './../../../components/Button/ReplyButton';

import { logAction } from '../../../utils';

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
          actionType: 'email_quickreply',
          participantId: participantId,
          timeDelta: Date.now() - startTime,
          emailId: emailId,
          message: reply.message,
          timestamp: new Date(),
        })
      }
    />
  ));
};

export default QuickReply;
