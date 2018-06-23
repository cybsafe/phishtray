import React, { Component } from 'react';
import { Button } from 'carbon-components-react';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <Button>
          Primary button
        </Button>
      </div>
    );
  }
}

export default App;
