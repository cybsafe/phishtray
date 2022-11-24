import React from 'react';
import { connect } from 'react-redux';
import styled from 'react-emotion';
import CustomMarkdown from '../../../Markdown/CustomMarkdown';

export const Wrapper = styled('section')`
  min-height: calc(100vh - 120px);
  background-color: #ffffff;
  overflow-y: scroll;
  position: relative;
  padding: 60px 0;
`;

export const Container = styled('div')`
  max-width: 700px;
  margin: 0 auto;
  width: 100%;
  text-align: center;
`;

const Title = styled('h1')`
  margin-bottom: 60px;
  font-size: 48px;
  color: #262939;
`;

const Warning = props => {
  const active = props.threads.filter(
    thread => thread.id === props.activeThread
  );
  const { webPage } = active[0].threadProperties;
  return (
    <Wrapper>
      <Container>
        <Title>{webPage.title}</Title>
        <CustomMarkdown source={webPage.content} />
      </Container>
    </Wrapper>
  );
};

export default connect(state => ({
  threads: state.exercise.threads,
  activeThread: state.exercise.activeThread,
}))(Warning);
