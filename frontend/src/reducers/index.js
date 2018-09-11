import { combineReducers } from 'redux';
import exercise from './exercise';
import inbox from './inbox';
import fileManager from './fileManager';
import ui from './ui';

const rootReducer = combineReducers({
  exercise,
  inbox,
  fileManager,
  ui,
});
export default rootReducer;
