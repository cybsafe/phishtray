// @flow
import React, { Component } from 'react';
import { Route, Switch, type Match, type history } from 'react-router-dom';
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
import {
  getLastRefreshed,
  getExercise,
} from '../../selectors/exerciseSelectors';
import type { ExerciseState } from '../../types/exerciseTypes';

import {
  getExerciseData,
  startCountdown,
  tickTimer,
} from '../../actions/exerciseActions';
import { postFormData, logAction } from '../../utils';
import actionTypes from '../../config/actionTypes';

const Container = styled('div')({
  margin: 'auto',
  minHeight: '100%',
  marginTop: '20px',
  width: '768px',
  backgroundColor: '#f5f7fa',
});

const Title = styled('h1')({
  display: 'flex',
  fontSize: ' 2.25rem',
  lineHeight: 1.25,
  marginBottom: '35px',
  fontWeight: 300,
});

const MarkdownContainer = styled('div')`
  display: flex;
  h1,
  h2,
  h3,
  h4 {
    margin: 10px 0;
    font-weight: bold;
  }
  p {
    padding: 10px 0px;
    line-height: 2;
  }
  ol {
    list-style: decimal;
  }
  ul {
    list-style: disc;
  }
  li {
    margin-top: 10px;
    margin-bottom: 10px;
    margin-left: 20px;
    line-height: 2;
  }
  img {
    width: 100%;
    margin: 20px 0;
  }
`;

const Divider = styled('p')({
  borderBottom: '1px solid #CCC',
  margin: '20px 0px 20px',
});

const Subtitle = styled('p')({
  display: 'flex',
  fontSize: ' 1.25rem',
  lineHeight: 1,
  paddingBottom: '15px',
  fontWeight: 300,
});

const FormContainer = styled('div')({
  display: 'flex',
  margin: 'auto',
  width: '384px',
  lineHeight: 1,
  paddingBottom: '15px',
  paddingTop: '15px',
});

type Props = {
  exercise: Object,
  match: Match,
  history: history,
  isLoaded: *,
  getExerciseData: (*) => void,
  startCountdown: (*) => void,
};

injectGlobal`
  #root > div:first-child {
    overflow-y: scroll !important;
  }
`;

export class Exercise extends Component<Props> {
  constructor(props: Props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    const { exerciseUuid } = this.props.match.params;
    this.props.getExerciseData(exerciseUuid);
  }

  componentDidUpdate() {
    if (this.state && Object.keys(this.state).length === 0) {
      this.props.exercise.profileForm &&
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

  nextPath(path: string) {
    this.props.history.push(path);
  }

  userInput = (event: SyntheticInputEvent<*>) => {
    this.setState({
      [event.target.id]: {
        id: event.target.name,
        value: event.target.value,
      },
    });
  };

  handleSubmit = (event: SyntheticInputEvent<*>) => {
    event && event.preventDefault();

    logAction({
      participantId: this.props.participantId,
      actionType: actionTypes.experimentStarted,
      timestamp: new Date(),
      timeDelta: Date.now() - this.props.startTime,
    });

    setInterval(() => {
      this.props.tickTimer(5); //this is way too high, demo purposes
    }, 5 * 1000);

    const { exercise } = this.props;
    exercise.startTime || this.props.startCountdown(exercise.lengthMinutes);

    const data = {
      profileForm:
        this.state &&
        Object.keys(this.state).map(
          answerKey => this.state && this.state[answerKey]
        ),
    };

    postFormData(
      `/api/v1/participants/${exercise.participant}/extend-profile/`,
      data
    );

    this.props.history.replace('/');
  };

  WelcomeForm = (exercise: ExerciseState) => (
    <Container>
      <Title>{exercise.title}</Title>
      <Tile>
        <MarkdownContainer>
          <ReactMarkdown>{exercise.description}</ReactMarkdown>
        </MarkdownContainer>

        {exercise.profileForm ? (
          <Form
            onSubmit={this.handleSubmit}
            id={exercise.id && `exercise-${exercise.id}`}
          >
            {exercise.profileForm.map(item => {
              switch (item.questionType) {
                case 0: // number
                  return (
                    <FormContainer key={item.id}>
                      <TextInput
                        type="number"
                        min={16}
                        labelText={item.question}
                        id={`${item.id}`}
                        name={`${item.id}`}
                        onChange={this.userInput}
                        onClick={this.userInput}
                        required={item.required}
                      />
                    </FormContainer>
                  );

                case 1: // text
                  return (
                    <FormContainer key={item.id}>
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
        ) : (
          this.handleSubmit()
        )}
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
                <Subtitle>Description</Subtitle>
                <MarkdownContainer>
                  <ReactMarkdown>{exercise.description}</ReactMarkdown>
                </MarkdownContainer>
                <Divider />
                <Subtitle>Introduction</Subtitle>
                <MarkdownContainer>
                  <ReactMarkdown>{exercise.introduction}</ReactMarkdown>
                </MarkdownContainer>
                <Divider />
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
    startTime: state.exercise.startTime,
    participantId: state.exercise.participant,
  }),
  { getExerciseData, startCountdown, tickTimer }
)(Exercise);
