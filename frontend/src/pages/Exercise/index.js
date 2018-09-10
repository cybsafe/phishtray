import React, { Component, Fragment } from 'react';
import styled, { css } from 'react-emotion';
import { connect } from 'react-redux';
import { InlineLoading, Button } from 'carbon-components-react';
import ReactMarkdown from 'react-markdown';

import {
  loadExercises,
  getLastRefreshed,
  getExercise,
} from '../../reducers/exercise';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'column',
  minHeight: '100%',
  margin: 50,
  marginTop: 0,
});

export class Exercise extends Component {
  async componentDidMount() {
    await this.props.loadExercises();
  }

  render() {
    const { exercise, isLoaded } = this.props;

    if (!isLoaded) {
      return (
        <Container>
          <InlineLoading
            className={css({
              color: 'black',
              justifyContent: 'center',
              '& svg': { stroke: 'black !important' },
            })}
            description="Loading"
          />
        </Container>
      );
    }

    return (
      <Fragment>
        <Container>
          <ReactMarkdown>{exercise.content}</ReactMarkdown>
          <Button>Start</Button>
        </Container>
      </Fragment>
    );
  }
}

export default connect(
  state => ({
    exercise: getExercise(state),
    isLoaded: getLastRefreshed(state) !== null,
  }),
  { loadExercises }
)(Exercise);
