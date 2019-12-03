import React, { useState } from 'react';
import { connect } from 'react-redux';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLock } from '@fortawesome/free-solid-svg-icons';
import {
  Wrapper,
  Container,
  Title,
  Input,
  Form,
  SubmitButton,
  Clear,
} from './ui';

import { logAction } from '../../../../utils';
import actionTypes from '../../../../config/actionTypes';
import CustomMarkdown from '../../../Markdown/CustomMarkdown';
import { closeWebpage } from '../../../../actions/uiActions';

type Props = {
  closeWebpage: () => void,
  activeThread: string,
  threads: Array<*>,
  startTime: Date,
  participantId: Number,
};

function Blocked({
  closeWebpage,
  activeThread,
  threads,
  startTime,
  participantId,
}: Props) {
  const [code, setCode] = useState(null);
  const [error, setError] = useState(false);

  const active = threads.filter(thread => thread.id === activeThread);
  const { threadProperties, id } = active[0];
  const releaseCodes = threadProperties.releaseCodes.map(
    item => item.releaseCode
  );

  const handleChange = e => {
    setCode(e.target.value);
  };

  const handleSubmit = e => {
    e.preventDefault();
    if (releaseCodes.includes(code)) {
      logAction({
        actionType: actionTypes.trainingReleaseCodeConfirm,
        emailId: id,
        releaseCodeEntered: code,
        participantId: participantId,
        timeDelta: Date.now() - startTime,
        timestamp: new Date(),
      });
      closeWebpage();
    } else {
      setError(true);
    }
  };

  if (!active[0].threadProperties.webPage) {
    // I believe it will never fall here cause the thread doesn't have webPage
    return null;
  }

  return (
    <Wrapper>
      <Container>
        <FontAwesomeIcon icon={faLock} size="2x" color="#ffffff" />

        <Title>{threadProperties.webPage.title}</Title>

        <CustomMarkdown
          light
          marginBottom
          source={threadProperties.webPage.content}
        />

        <Form onSubmit={handleSubmit}>
          <Input
            onChange={handleChange}
            placeholder="Enter the code"
            invalid={error}
            invalidText="Incorrect code provided"
            labelText=""
            id="1"
          />
          <Clear>
            <SubmitButton type="submit">Submit</SubmitButton>
          </Clear>
        </Form>
      </Container>
    </Wrapper>
  );
}

export default connect(
  state => ({
    activeThread: state.exercise.activeThread,
    threads: state.exercise.threads,
    startTime: state.exercise.startTime,
    participantId: state.exercise.participant,
  }),
  { closeWebpage }
)(Blocked);
