import React from 'react';
import ReactDOM from 'react-dom';
import 'carbon-components/css/carbon-components.css';
import './global.css';

import App from './App';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();
