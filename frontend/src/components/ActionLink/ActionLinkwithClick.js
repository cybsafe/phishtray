// @flow
import React from 'react';
import styled from 'react-emotion';
import { connect } from 'react-redux';
import { logAction, selectWebpageType } from '../../utils';

import { setInlineNotification } from '../../actions/exerciseActions';
import { showWebpage } from '../../actions/uiActions';

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
  setInlineNotification: (term: string) => void,
  threadId: string,
  remove?: string,
  secondary?: string,
  onReplyPress: () => void,
  threads: Array,
  activeThread?: string,
  showWebpage: () => void,
};

const ActionLink = styled('button')`
  display: block;
  text-decoration: none;
  color: #b8b8b8;
  font-size: 16px;
  font-weight: bold;
  letter-spacing: 1.1px;
  padding: 10px;
  border: 1px solid transparent;
  cursor: pointer;

  &:hover {
    color: ${({ secondary }) => (secondary ? '#eb4934' : '#3d70b2')};
    border: 1px solid ${({ secondary }) => (secondary ? '#eb4934' : '#3d70b2')};
  }
  &:focus {
    outline: none;
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
  setInlineNotification,
  threads,
  activeThread,
  showWebpage,
  ...restProps
}: Props) {
  const active = threads.filter(thread => thread.id === activeThread);

  const {
    interceptExercise,
    releaseCodes,
    webPage,
  } = active[0].threadProperties;
  return (
    <ActionLink
      onClick={() => {
        logAction({
          actionType: data.actionType,
          participantId: data.participantId,
          timeDelta: Date.now() - data.startTime,
          emailId: data.emailId,
          timestamp: new Date(),
        });
        remove && markThreadAsDeleted(threadId) && markThreadAsInactive();
        onReplyPress && onReplyPress();
        setInlineNotification && setInlineNotification(title);
        webPage &&
          selectWebpageType(
            interceptExercise,
            releaseCodes,
            showWebpage,
            data.actionType
          );
      }}
      {...restProps}
    >
      {title}
    </ActionLink>
  );
}

export default connect(
  state => ({
    threads: state.exercise.threads,
    activeThread: state.exercise.activeThread,
  }),
  {
    setInlineNotification,
    showWebpage,
  }
)(ActionLinkwithClick);
