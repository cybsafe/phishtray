import React from 'react';

import Button from './../../../components/Button/ReplyButton';

type Props = {
  replies: Array<*>,
};

const QuickReply = (props: Props) =>
  props.replies &&
  props.replies.map(
    reply =>
      reply.id && reply.type && reply.message && <Button content={reply.type} />
  );

export default QuickReply;
