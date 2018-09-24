import { createSelector } from 'reselect';

const exerciseSelector = state => state.exercise;

export const getLastRefreshed = createSelector(
  exerciseSelector,
  exercise => exercise.lastRefreshed
);

export const getExercise = createSelector(
  exerciseSelector,
  exercise => exercise
);

export const getExerciseTimer = createSelector(
  exerciseSelector,
  exercise => exercise.timer
);

export const getThreads = createSelector(exerciseSelector, exercise =>
  exercise.threads.filter(
    thread =>
      exercise.emailRevealTimes.filter(time => time.emailId === thread.id)[0]
        .revealTime <= exercise.timer
  )
);

export const getThread = createSelector(
  [exerciseSelector, (_, props) => props.threadId, getExerciseTimer],
  (exercise, threadId) =>
    exercise.threads.find(
      thread =>
        thread.id === threadId &&
        exercise.emailRevealTimes.filter(time => time.emailId === thread.id)[0]
          .revealTime <= exercise.timer
    )
);
