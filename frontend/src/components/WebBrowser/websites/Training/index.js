import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import CustomMarkdown from '../../../Markdown/CustomMarkdown';
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

import { closeWebpage } from '../../../../actions/uiActions';
import { logAction } from '../../../../utils';
import actionTypes from '../../../../config/actionTypes';

function Training() {
  const { activeThread, threads, startTime } = useSelector(
    state => state.exercise
  );
  const participantId = useSelector(state => state.exercise.participant);
  const dispatch = useDispatch();

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
      dispatch(closeWebpage());
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
        <FontAwesomeIcon icon={faLock} size="2x" color="#999999" />

        <Title>{threadProperties.webPage.title}</Title>

        <CustomMarkdown source={threadProperties.webPage.content} />

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

export default Training;
