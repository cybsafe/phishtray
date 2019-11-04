import React, { useState } from 'react';
import { connect } from 'react-redux';
import ReactMarkdown from 'react-markdown';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLock } from '@fortawesome/free-solid-svg-icons';
import {
  Wrapper,
  Container,
  Title,
  Text,
  Input,
  Form,
  MarkDownContainer,
  SubmitButton,
} from './ui';

import { closeWebpage } from '../../../../actions/uiActions';

type Props = {
  closeWebpage: () => void,
  activeThread: string,
  threads: Array<*>,
};

function Training({ closeWebpage, activeThread, threads }: Props) {
  const [code, setCode] = useState(null);
  const [error, setError] = useState(false);

  const active = threads.filter(thread => thread.id === activeThread);
  const { threadProperties } = active[0];
  const releaseCodes = threadProperties.releaseCodes.map(
    item => item.releaseCode
  );

  const handleChange = e => {
    setCode(e.target.value);
  };

  const handleSubmit = e => {
    e.preventDefault();
    if (releaseCodes.includes(code)) {
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

        <MarkDownContainer>
          <ReactMarkdown source={threadProperties.webPage.content} />
        </MarkDownContainer>

        <Form onSubmit={handleSubmit}>
          <Input
            onChange={handleChange}
            placeholder="Enter the code"
            invalid={error}
            invalidText="Incorrect code provided"
            labelText=""
            id="1"
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
)(Training);
