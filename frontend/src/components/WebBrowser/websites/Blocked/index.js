import React, { useState } from 'react';
import { connect } from 'react-redux';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLock } from '@fortawesome/free-solid-svg-icons';
import {
  Wrapper,
  Container,
  Title,
  Text,
  Input,
  Form,
  SubmitButton,
} from './ui';

import { closeWebpage } from '../../../../actions/uiActions';

type Props = {
  closeWebpage: () => void,
  activeThread: string,
  threads: Array<*>,
};

function Blocked({ closeWebpage, activeThread, threads }: Props) {
  const [code, setCode] = useState(null);
  const [error, setError] = useState(false);

  const handleChange = e => {
    setCode(e.target.value);
  };

  const handleSubmit = e => {
    e.preventDefault();
    if (code === 'benthehero') {
      closeWebpage();
    } else {
      setError(true);
    }
  };

  const active = threads.filter(thread => thread.id === activeThread);

  console.log({ active });

  return (
    <Wrapper>
      <Container>
        <FontAwesomeIcon icon={faLock} size="2x" color="#ffffff" />

        <Title>Your task has been locked</Title>

        <Text>
          You fell for a phishing simulation, you must now complete the
          following course and your task progress on the task is correctly until
          course completion.
        </Text>

        <Form onSubmit={handleSubmit}>
          <Input
            onChange={handleChange}
            placeholder="Enter the code"
            invalid={error}
            invalidText="Wrong code provided"
          />
          <SubmitButton type="submit">Submit</SubmitButton>
        </Form>
      </Container>
    </Wrapper>
  );
}

export default connect(
  state => ({
    activeThread: state.exercise.activeThread,
    threads: state.exercise.threads,
  }),
  { closeWebpage }
)(Blocked);
