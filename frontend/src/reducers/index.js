import { combineReducers } from 'redux';
import exercise from './exerciseReducer';
import fileManager from './fileManagerReducer';
import ui from './uiReducer';
import debrief from './debriefReducer';

const rootReducer = combineReducers({
  exercise,
  debrief,
  fileManager,
  ui,
});
export default rootReducer;
