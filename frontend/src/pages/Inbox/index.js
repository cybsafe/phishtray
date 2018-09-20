import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import styled, { css } from 'react-emotion';
import { connect } from 'react-redux';
import { InlineLoading } from 'carbon-components-react';

import {
  getThreads,
  getLastRefreshed,
  loadThreads,
} from '../../reducers/inbox';

import EmailChain from './components/EmailChain';
import EmailListItem from './components/EmailListItem';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  height: '100%',
});

const EmailList = styled('div')({
  flex: 0,
  flexBasis: 280,
  backgroundColor: '#1B87EC',
  minHeight: '100%',
});

const EmailContainer = styled('div')({
  flex: 1,
  overflow: 'auto',
  paddingBottom: 80,
});

export class Inbox extends Component {
  async componentDidMount() {
    await this.props.loadThreads();
  }

  render() {
    const { match, threads, isLoaded } = this.props;

    if (!isLoaded) {
      return (
        <Container>
          <EmailList>
            <InlineLoading
              className={css({
                color: '#fff',
                justifyContent: 'center',
                marginTop: '20%',
                '& svg': { stroke: '#fff !important' },
              })}
              description="Loading"
            />
          </EmailList>
          <EmailContainer />
        </Container>
      );
    }

    return (
      <Container>
        <EmailList>
          {threads.map(thread => (
            <EmailListItem
              key={thread.id}
              email={thread}
              onOpenParams={{
                startTime: this.props.startTime,
                participantId: this.props.participantId,
              }}
            />
          ))}
        </EmailList>
        <EmailContainer>
          <Route path={`${match.url}/:emailId`} component={EmailChain} />
        </EmailContainer>
      </Container>
    );
  }
}

export default connect(
  state => ({
    threads: getThreads(state),
    isLoaded: getLastRefreshed(state) !== null,
    startTime: state.countdown.startTime,
    participantId: state.exercise.participant,
  }),
  { loadThreads }
)(Inbox);
