import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import styled, { css } from 'react-emotion';
import { connect } from 'react-redux';
import {
  InlineLoading,
  Button,
  NumberInput,
  TextInput,
  Form,
  Tile,
} from 'carbon-components-react';
import ReactMarkdown from 'react-markdown';

import {
  loadExercises,
  getLastRefreshed,
  getExercise,
} from '../../reducers/exercise';

const Container = styled('div')({
  margin: 'auto',
  minHeight: '100%',
  marginTop: '20px',
  width: '768px',
  backgroundColor: '#f5f7fa',
});

const Title = styled('h1')({
  display: 'block',
  fontSize: ' 2.25rem',
  lineHeight: 1.25,
  marginBottom: '35px',
  fontWeight: 300,
});

const Subtitle = styled('h1')({
  display: 'block',
  fontSize: ' 1.25rem',
  lineHeight: 1,
  paddingBottom: '15px',
  fontWeight: 300,
  borderBottom: '1px solid grey',
});

const FormContainer = styled('div')({
  display: 'block',
  margin: 'auto',
  width: '384px',
  lineHeight: 1,
  paddingBottom: '15px',
  paddingTop: '15px',
});

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
    await this.props.exercise.profile_form.map(item =>
      this.setState({
        [item.id]: {
          id: item.id,
          value: '',
        },
      })
    );
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

    fetch('/api/form-submit-url', {
      method: 'POST',
      body: data,
    });

    this.nextPath('/');
  };

  WelcomeForm = exercise => (
    <Container>
      <Title>{exercise.title}</Title>
      <Tile>
        <Subtitle>{exercise.description}</Subtitle>
        <Form onSubmit={this.handleSubmit} id={`exercise-${exercise.id}`}>
          {exercise.profile_form.map(item => {
            switch (item.question_type) {
              case 'number':
                return (
                  <FormContainer>
                    <Number
                      className={css(`width: 100%`)}
                      label={item.question}
                      min={0}
                      id={`${item.id}`}
                      name={`${item.id}`}
                      onChange={this.userInput}
                      onClick={this.userInput}
                      required={item.required}
                      invalidText="Please input a number value"
                    />
                  </FormContainer>
                );

              case 'string':
                return (
                  <FormContainer>
                    <TextInput
                      id={`${item.id}`}
                      labelText={item.question}
                      name={`${item.id}`}
                      onChange={this.userInput}
                      required={item.required}
                    />
                  </FormContainer>
                );
              default:
                return {};
            }
          })}
          <Button
            className={css(`display: flex !important; margin-left: auto`)}
            type="submit"
          >
            Click here to start the E-tray
          </Button>
        </Form>
      </Tile>
    </Container>
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
      <Switch>
        <Route
          exact
          path={`${match.url}`}
          render={() => (
            <Container>
              <Title>{exercise.title}</Title>
              <Tile>
                <Subtitle>{exercise.description}</Subtitle>

                <ReactMarkdown>{exercise.introduction}</ReactMarkdown>
                <hr />
                <p>This exercise will take: {exercise.time}</p>
                <Button
                  className={css(`display: flex !important; margin-left: auto`)}
                  onClick={() => this.nextPath('/welcome/form')}
                >
                  Continue
                </Button>
              </Tile>
            </Container>
          )}
        />
        <Route
          path={`${match.url}/form`}
          render={() => <Container>{this.WelcomeForm(exercise)}</Container>}
        />
      </Switch>
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
