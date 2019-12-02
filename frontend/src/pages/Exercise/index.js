// @flow
import React, { useState, useEffect } from 'react';
import { Route, Switch } from 'react-router-dom';
import styled, { css, injectGlobal } from 'react-emotion';
import { useSelector, useDispatch } from 'react-redux';
import {
  InlineLoading,
  Button,
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

injectGlobal`
  #root > div:first-child {
    overflow-y: scroll !important;
  }
`;

type Props = {
  match: object,
  history: object,
};

function Exercise({ match, history }: Props) {
  const [item, setItem] = useState([]);
  const exercise = useSelector(state => getExercise(state));
  const isLoaded = useSelector(state => getLastRefreshed(state) !== null);
  const startTime = useSelector(state => state.exercise.startTime);
  const participantId = useSelector(state => state.exercise.participant);
  const dispatch = useDispatch();

  useEffect(() => {
    const { exerciseUuid } = match.params;
    dispatch(getExerciseData(exerciseUuid));
  }, [dispatch, match.params]);

  useEffect(() => {
    if (item && Object.keys(item).length === 0) {
      exercise.profileForm &&
        exercise.profileForm.map(item =>
          setItem({
            [item.id]: {
              id: item.id,
              value: '',
            },
          })
        );
    }
  }, [item, exercise]);

  const nextPath = (path: string) => {
    history.push(path);
  };

  const userInput = event => {
    setItem({
      [event.target.id]: {
        id: event.target.name,
        value: event.target.value,
      },
    });
  };

  const handleSubmit = (event: SyntheticInputEvent<*>) => {
    event && event.preventDefault();

    logAction({
      participantId,
      actionType: actionTypes.experimentStarted,
      timestamp: new Date(),
      timeDelta: Date.now() - startTime,
    });

    setInterval(() => {
      dispatch(tickTimer(5)); //this is way too high, demo purposes
    }, 5 * 1000);

    exercise.startTime || dispatch(startCountdown(exercise.lengthMinutes));

    const data = {
      profileForm:
        item && Object.keys(item).map(answerKey => item && item[answerKey]),
    };

    postFormData(
      `/api/v1/participants/${exercise.participant}/extend-profile/`,
      data
    );

    history.replace('/');
  };

  const WelcomeForm = (exercise: ExerciseState) => (
    <Container>
      <Title>{exercise.title}</Title>
      <Tile>
        <Subtitle>Demographic Information</Subtitle>
        {exercise.profileForm ? (
          <Form
            onSubmit={handleSubmit}
            id={exercise.id && `exercise-${exercise.id}`}
          >
            {exercise.profileForm.map(item => {
              switch (item.questionType) {
                case 0: // number
                  return (
                    <FormContainer key={item.id}>
                      <TextInput
                        type="number"
                        labelText={item.question}
                        id={`${item.id}`}
                        name={`${item.id}`}
                        onChange={userInput}
                        onClick={userInput}
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
                        onChange={userInput}
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
          handleSubmit()
        )}
      </Tile>
    </Container>
  );

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
                onClick={() => nextPath(`/welcome/${exercise.id}/form`)}
              >
                Continue
              </Button>
            </Tile>
          </Container>
        )}
      />
      <Route
        path={`${match.url}/form`}
        render={() => <Container>{WelcomeForm(exercise)}</Container>}
      />
    </Switch>
  );
}

export default Exercise;
