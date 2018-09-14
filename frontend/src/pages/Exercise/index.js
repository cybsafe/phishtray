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

const Title = styled('h1')({ display: 'block' });

const Number = styled(NumberInput)`
  .bx--number__controls {
    visibility: hidden;
  }
`;

export class Exercise extends Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  async componentDidMount() {
    await this.props.loadExercises();
    await this.props.exercise.form.map(item => {
      this.setState(previousState => ({
        ...previousState,
        [item.key]: '',
      }));
    });
  }

  nextPath(path) {
    this.props.history.push(path);
  }

  userInput = event => {
    this.setState({
      [event.target.name]: event.target.value,
    });
  };

  handleSubmit = () => {
    const data = this.state;

    fetch('/api/form-submit-url', {
      method: 'POST',
      body: data,
    });

    this.nextPath('/');
  };

  WelcomeForm = exercise => (
    <Fragment>
      <Title>{exercise.title}</Title>
      <Form onSubmit={this.handleSubmit} id={`exercise-${exercise.id}`}>
        {exercise.form.map(item => {
          switch (item.type) {
            case 'number':
              return (
                <Number
                  label={item.label}
                  min={0}
                  id={`${item.key}`}
                  name={`${item.key}`}
                  onChange={this.userInput}
                  onClick={this.userInput}
                  invalidText="Please input a number value"
                />
              );

            case 'string':
              return (
                <TextInput
                  id={`${item.key}`}
                  labelText={item.label}
                  name={`${item.key}`}
                  onChange={this.userInput}
                />
              );
          }
        })}
        <Button type="submit">Click here to start the E-tray</Button>
      </Form>
    </Fragment>
  );

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
                <Title>{exercise.title}</Title>
                <ReactMarkdown>{exercise.introduction}</ReactMarkdown>
                <Button onClick={() => this.nextPath('/welcome/form')}>
                  Continue
                </Button>
              </Container>
            )}
          />
          <Route
            path={`${match.url}/form`}
            render={() => <Container>{this.WelcomeForm(exercise)}</Container>}
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
