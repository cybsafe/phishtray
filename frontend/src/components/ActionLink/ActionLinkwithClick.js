// @flow
import React from 'react';
import styled from 'react-emotion';
import { Link } from 'react-router-dom';
import { logAction } from '../../utils';

type Props = {
  data: {
    actionType: String,
    emailId: String,
    participantId: String,
    startTime: number,
  },
  title: string,
  markThreadAsDeleted: (threadId: string) => void,
  markThreadAsInactive: () => void,
  threadId: string,
  remove?: string,
  secondary?: string,
};

const ActionLink = styled(Link)`
  display: block;
  text-decoration: none;
  color: #b8b8b8;
  font-weight: bold;
  letter-spacing: 1.1px;
  padding: 10px 10px;
  border: 1px solid transparent;

  &:hover {
    color: ${({ secondary }) => (secondary ? '#eb4934' : '#3d70b2')};
    border: 1px solid ${({ secondary }) => (secondary ? '#eb4934' : '#3d70b2')};
  }
  &:active {
    color: ${({ secondary }) => (secondary ? '#eb4934' : '#3d70b2')};
    border: 1px solid
      ${({ secondary }) => (secondary ? '#eb4934' : 'rgba(24, 104, 184, 0.1)')};
    background-color: ${({ secondary }) =>
      secondary ? 'rgba(235, 72, 51, 0.1)' : 'rgba(24, 104, 184, 0.1)'};
  }
`;

function ActionLinkwithClick({
  data,
  title,
  markThreadAsDeleted,
  markThreadAsInactive,
  threadId,
  remove,
  onReplyPress,
  ...restProps
}: Props) {
  return (
    <ActionLink
      to={
        remove
          ? {
              pathname: '/inbox',
            }
          : {}
      }
      onClick={() => {
        logAction({
          actionType: data.actionType,
          participantId: data.participantId,
          timeDelta: Date.now() - data.startTime,
          emailId: data.emailId,
          timestamp: new Date(),
        });
        remove && markThreadAsDeleted(threadId) && markThreadAsInactive();
        onReplyPress();
      }}
      {...restProps}
    >
      {title}
    </ActionLink>
  );
}

export default ActionLinkwithClick;
