import React from 'react';
import { connect } from 'react-redux';
import Markdown from 'react-markdown';
import styled from 'react-emotion';

const Container = styled('div')({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  height: '100%',
  backgroundColor: '#fff',
  boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.1)',
  padding: '1rem',
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

class Afterward extends React.Component<Props> {
  componentDidMount() {
    clearInterval();
  }

  render() {
    return (
      <Container>
        <Title>Thanks for taking the exercise.</Title>
        {this.props.afterwardMessage && (
          <Markdown source={this.props.afterwardMessage} />
        )}
      </Container>
    );
  }
}

export default connect(
  state => ({
    afterwardMessage: state.exercise.afterward,
  }),
  {}
)(Afterward);
