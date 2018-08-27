const express = require('express');
const expressApp = express();
const cors = require('cors');
var bodyParser = require('body-parser');

class Server {
  constructor() {
    this.app = expressApp;
    this.app.use(bodyParser.json()); // support json encoded bodies
    this.app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies

    this.applyMiddleware();
    this.assignEndpoints();
  }

  applyMiddleware() {
    this.app.use(cors());
  }

  assignEndpoints() {
    this.app.post('/exercise/:partyId/actions', (req, res) => {
      res.send(req.body);
    });
  }

  start() {
    this.app.listen(8282, () => {
      console.log('server online ++++++');
    });
  }
}

const server = new Server();
server.start();
