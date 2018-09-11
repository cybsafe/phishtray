import { combineReducers } from 'redux';
import exercise from './exercise';
import inbox from './inbox';
import fileManager from './fileManager';

const rootReducer = combineReducers({
  exercise,
  inbox,
  fileManager,
});
export default rootReducer;
