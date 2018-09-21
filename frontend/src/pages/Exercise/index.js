import React, { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import styled, { css, injectGlobal } from 'react-emotion';
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

import { getLastRefreshed, getExercise } from '../../reducers/exercise';

import { getExerciseData, startCountdown } from '../../actions/exerciseActions';
import { postFormData } from '../../utils';

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

type Props = {
  exercise: Object,
  isLoaded: *,
  loadExercises: (*) => void,
  startCountdown: (*) => void,
};

injectGlobal`
  #root > div:first-child {
    overflow-y: scroll !important;
  }
`;

export class Exercise extends Component<Props> {
  constructor(props) {
    super(props);
    this.state = {};
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    const { exerciseUuid } = this.props.match.params;
    this.props.getExerciseData(exerciseUuid);
  }

  componentDidUpdate() {
    if (Object.keys(this.state).length === 0) {
      this.props.exercise.profileForm.map(item =>
        this.setState({
          [item.id]: {
            id: item.id,
            value: '',
          },
        })
      );
    }
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

  handleSubmit = event => {
    event.preventDefault();

    const { exercise } = this.props;
    this.props.startCountdown(exercise.lengthMinutes);

    const data = {
      profileForm: Object.keys(this.state).map(
        answerKey => this.state[answerKey]
      ),
    };

    postFormData(
      `/api/v1/participants/${exercise.participant}/extend-profile/`,
      data
    );

    this.nextPath('/');
  };

  WelcomeForm = exercise => (
    <Container>
      <Title>{exercise.title}</Title>
      <Tile>
        <Subtitle>{exercise.description}</Subtitle>
        <Form onSubmit={this.handleSubmit} id={`exercise-${exercise.id}`}>
          {exercise.profileForm.map(item => {
            switch (item.questionType) {
              case 0: // number
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

              case 1: // text
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
                <p>This exercise will take: {exercise.lengthMinutes} mins</p>
                <Button
                  className={css(`display: flex !important; margin-left: auto`)}
                  onClick={() => this.nextPath(`/welcome/${exercise.id}/form`)}
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
  { getExerciseData, startCountdown }
)(Exercise);
