import React from 'react';

import Button from './../../../components/Button/ReplyButton';

type Props = {
  replies: Array<*>,
  subject: string,
  emailAdd: () => any,
};

const QuickReply = (props: Props) =>
  props.replies.map(reply => (
    <Button
      key={reply.id}
      type={reply.type}
      content={reply.message}
      emailAdd={props.emailAdd}
      subject={props.subject}
    />
  ));

export default QuickReply;
