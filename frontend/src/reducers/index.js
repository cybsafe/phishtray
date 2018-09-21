import { combineReducers } from 'redux';
import exercise from './exerciseReducer';
import inbox from './inboxReducer';
import fileManager from './fileManagerReducer';
import ui from './uiReducer';

const rootReducer = combineReducers({
  exercise,
  inbox,
  fileManager,
  ui,
});
export default rootReducer;
