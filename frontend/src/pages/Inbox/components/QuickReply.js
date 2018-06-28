import React from 'react';

import Button from './../../../components/Button/ReplyButton';

type Props = {
  replies: Array<*>,
};

const QuickReply = (props: Props) =>
  props.replies.map(reply => (
    <Button key={reply.id} type={reply.type} content={reply.message} />
  ));

export default QuickReply;
