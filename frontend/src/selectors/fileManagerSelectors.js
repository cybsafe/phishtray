import { createSelector } from 'reselect';

const filesSelector = state => state.fileManager;

export const getFiles = createSelector(
  filesSelector,
  fileManager => fileManager.files
);

export const getLastRefreshed = createSelector(
  filesSelector,
  fileManager => fileManager.lastRefreshed
);

export const getModal = createSelector(
  filesSelector,
  fileManager => fileManager.modal
);
