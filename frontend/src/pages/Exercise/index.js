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
    await this.props.exercise.profile_form.map(item => {
      this.setState({
        [item.id]: {
          id: item.id,
          value: '',
        },
      });
    });
  }

  nextPath(path) {
    this.props.history.push(path);
  }

  userInput = event => {
    this.setState({
      [event.target.id]: {
        id: event.target.name,
        value: event.target.value,
      },
    });
  };

  handleSubmit = () => {
    const data = Object.keys(this.state).map(answer => this.state[answer]);

    console.log(data);
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
        {exercise.profile_form.map(item => {
          switch (item.field_type) {
            case 'number':
              return (
                <Number
                  label={item.label}
                  min={0}
                  id={`${item.id}`}
                  name={`${item.id}`}
                  onChange={this.userInput}
                  onClick={this.userInput}
                  required={item.required}
                  invalidText="Please input a number value"
                />
              );

            case 'string':
              return (
                <TextInput
                  id={`${item.id}`}
                  labelText={item.label}
                  name={`${item.id}`}
                  onChange={this.userInput}
                  required={item.required}
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
