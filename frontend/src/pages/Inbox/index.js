import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import styled, { css } from 'react-emotion';
import { connect } from 'react-redux';
import { InlineLoading } from 'carbon-components-react';
import { markThreadAsActive } from '../../actions/exerciseActions';
import {
  getThreads,
  getLastRefreshed,
} from '../../selectors/exerciseSelectors';

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
  overflow: 'auto',
});

const EmailContainer = styled('div')({
  flex: 1,
  overflow: 'auto',
  paddingBottom: 80,
});

export class Inbox extends Component {
  componentDidMount() {
    const { match, activeThread, history } = this.props;
    if (Object.keys(match.params).length === 0 && activeThread !== '') {
      history.push(`/inbox/${activeThread}`);
    }
  }
  render() {
    const { match, threads } = this.props;

    if (!threads) {
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
              markThreadAsActive={this.props.markThreadAsActive}
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
    startTime: state.exercise.startTime,
    participantId: state.exercise.participant,
    activeThread: state.exercise.activeThread,
  }),
  {
    markThreadAsActive,
  }
)(Inbox);
