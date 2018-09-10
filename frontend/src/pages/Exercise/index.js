import React, { Component } from 'react';
import styled, { css } from 'react-emotion';
import { connect } from 'react-redux';
import { InlineLoading } from 'carbon-components-react';

import {
  loadExercises,
  getLastRefreshed,
  getExercise,
} from '../../reducers/exercise';

const Container = styled('div')({
  display: 'flex',
  flexDirection: 'row',
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

    return <Container>{exercise.content}</Container>;
  }
}

export default connect(
  state => ({
    exercise: getExercise(state),
    isLoaded: getLastRefreshed(state) !== null,
  }),
  { loadExercises }
)(Exercise);
