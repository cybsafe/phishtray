import React, { Component, Fragment } from 'react';
import { Route, Switch } from 'react-router-dom';
import styled, { css } from 'react-emotion';
import { connect } from 'react-redux';
import {
  InlineLoading,
  Button,
  NumberInput,
  TextInput,
  Form,
} from 'carbon-components-react';
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

const WelcomeForm = ({ form, title }) => (
  <Fragment>
    {title}
    <Form onSubmit={this.handleSubmit}>
      {form.map(item => {
        switch (item.type) {
          case 'number':
            return <NumberInput label={item.label} />;

          case 'string':
            return <TextInput labelText={item.label} />;
        }
      })}
      <Button type="submit">Click here to start the E-tray</Button>
    </Form>
  </Fragment>
);

const Title = styled('div')({
  display: 'block',
});

export class Exercise extends Component {
  async componentDidMount() {
    await this.props.loadExercises();
  }

  nextPath(path) {
    this.props.history.push(path);
  }

  render() {
    const { exercise, isLoaded, match } = this.props;

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
        <Switch>
          <Route
            exact
            path={`${match.url}`}
            render={() => (
              <Container>
                <Title>{exercise.exercise}</Title>
                <ReactMarkdown>{exercise.content}</ReactMarkdown>
                <Button onClick={() => this.nextPath('/welcome/form')}>
                  Continue
                </Button>
              </Container>
            )}
          />
          <Route
            path={`${match.url}/form`}
            render={() => (
              <Container>
                <Title>{exercise.exercise}</Title>
                <WelcomeForm form={exercise.form} />
              </Container>
            )}
          />
        </Switch>
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
