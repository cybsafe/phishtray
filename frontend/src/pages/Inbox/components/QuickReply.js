import React from 'react';

import Button from './../../../components/Button/ReplyButton';

type Props = {
  replies: Array<*>,
  emailReply?: () => void,
};

const QuickReply = (props: Props) =>
  props.replies &&
  props.replies.map(
    reply =>
      reply.id &&
      reply.type &&
      reply.message && (
        <Button
          key={reply.id}
          content={reply.type}
          sendReply={props.emailReply}
        />
      )
  );

export default QuickReply;
