import { combineReducers } from 'redux';
import exercise from './exerciseReducer';
import fileManager from './fileManagerReducer';
import ui from './uiReducer';
import debrief from './debriefReducer';

const rootReducer = combineReducers({
  exercise,
  fileManager,
  ui,
  debrief,
});
export default rootReducer;
