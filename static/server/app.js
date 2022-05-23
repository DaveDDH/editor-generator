const express = require('express');
const actuator = require('express-actuator');
const fileUpload = require('express-fileupload');
const bodyParser = require('body-parser');
const cors = require('cors');

const dataRoutes = require('./routes/data');

require('dotenv').config();

const port = process.env.PORT || 8080;

const actuatorConfig = {
  basePath: '',
  infoGitMode: 'simple',
  infoBuildOptions: null,
  infoDateFormat: null,
  customEndpoints: [],
};

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(fileUpload({
  createParentPath: true
}));
app.use(actuator(actuatorConfig));
app.use(cors({
  origin: '*'
}));

app.use('/api/', dataRoutes);

function runApp() {  
  app.listen(port, () => {
    console.log(`App listening on port ${port}`)
  });
}

module.exports = {
  runApp: runApp,
};