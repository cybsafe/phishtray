import { combineReducers } from 'redux';
import exercise from './exercise';
import inbox from './inbox';
import fileManager from './fileManager';
import ui from './ui';
import countdown from './countdownReducer';

const rootReducer = combineReducers({
  exercise,
  inbox,
  fileManager,
  ui,
  countdown,
});
export default rootReducer;
