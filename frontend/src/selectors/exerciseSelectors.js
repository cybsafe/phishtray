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

export const getThreads = createSelector(
  exerciseSelector,
  exercise =>
    exercise.threads
      .filter(thread => thread.threadProperties.revealTime <= exercise.timer)
      .sort((a, b) => b.threadProperties.revealTime - a.threadProperties.revealTime)
);
export const getUnreadThreads = createSelector(
  exerciseSelector,
  exercise =>
    exercise.threads.filter(
      thread =>
        !thread.isRead && thread.threadProperties.revealTime <= exercise.timer
    ).length
);

export const getThread = createSelector(
  [exerciseSelector, (_, props) => props.threadId, getExerciseTimer],
  (exercise, threadId) => {
    return exercise.threads.find(
      thread =>
        thread.id === threadId &&
        exercise.threads.filter(
          thread => thread.threadProperties.revealTime <= exercise.timer
        )
    );
  }
);
