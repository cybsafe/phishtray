import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import styled from 'react-emotion';
import { connect } from 'react-redux';

import { getThreads, loadThreads } from '../../reducers/inbox';

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

const LoadingSpinner = () => <div>Loading</div>;

export class Inbox extends Component {
  state = {
    loading: true,
  };

  async componentDidMount() {
    await this.props.loadThreads();
    this.setState({
      loading: false,
    });
  }

  render() {
    const { match, threads } = this.props;
    const { loading } = this.state;

    if (loading) {
      return (
        <Container>
          <EmailList>
            <LoadingSpinner />
          </EmailList>
          <EmailContainer />
        </Container>
      );
    }

    return (
      <Container>
        <EmailList>
          {threads.map(thread => (
            <EmailListItem key={thread.id} email={thread} />
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
    threads: getThreads(state.inbox),
  }),
  { loadThreads }
)(Inbox);
