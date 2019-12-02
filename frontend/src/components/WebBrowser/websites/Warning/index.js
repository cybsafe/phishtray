import React from 'react';
import { connect } from 'react-redux';
import styled from 'react-emotion';
import CustomMarkdown from '../../../Markdown/CustomMarkdown';

const Container = styled('div')`
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 100%;
`;

const ContentWrapper = styled('div')`
  max-width: 648px;
`;

const Title = styled('h1')`
  margin-top: 80px;
  margin-bottom: 60px;
  color: #262939;
  font-size: 48px;
`;

const Warning = props => {
  const active = props.threads.filter(
    thread => thread.id === props.activeThread
  );
  const { webPage } = active[0].threadProperties;
  return (
    <Container>
      <ContentWrapper>
        <Title>{webPage.title}</Title>
        <CustomMarkdown source={webPage.content} />
      </ContentWrapper>
    </Container>
  );
};

export default connect(state => ({
  threads: state.exercise.threads,
  activeThread: state.exercise.activeThread,
}))(Warning);
