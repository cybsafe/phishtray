import React from 'react';
import { connect } from 'react-redux';
import ReactMarkdown from 'react-markdown';
import styled from 'react-emotion';
import { persistor } from '../../redux';
import { getRange } from '../../utils';

const Container = styled('div')({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  height: '100%',
  backgroundColor: '#fff',
  boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.1)',
  padding: '1rem',
  flexDirection: 'column',
});

const Title = styled('h1')({
  display: 'block',
  fontSize: ' 2.25rem',
  lineHeight: 1.25,
  marginBottom: '35px',
  fontWeight: 300,
});

type Props = {
  afterwardMessage: String,
};

const clearSessionStorage = async () => await sessionStorage.clear();

class Afterward extends React.Component<Props> {
  state = {
    message: '',
  };

  componentDidMount() {
    this.setState(
      {
        message: this.props.afterwardMessage,
      },
      () => {
        getRange(0, 100).map(i => clearInterval(i)); //bad habits
        clearSessionStorage().then(() => {
          sessionStorage.clear();
          persistor.purge();
        });
      }
    );
  }

  render() {
    return (
      <Container>
        <Title>Thanks for taking the exercise.</Title>
        {this.props.message && <ReactMarkdown source={this.state.message} />}
      </Container>
    );
  }
}

export default connect(
  state => ({
    afterwardMessage: state.exercise.afterword,
  }),
  {}
)(Afterward);
