const { runApp } = require('./app'); 
const { connect, mongoClient } = require('./mongoConnector');

async function run() {
  await connect();
  runApp();
}

async function exitHandler() {
  await mongoClient.close();
  console.log('\nDB connection closed.');
  process.exit();
}

process.on('exit', exitHandler.bind(null,{cleanup:true}));
process.on('SIGINT', exitHandler.bind(null, {exit:true}));
process.on('SIGUSR1', exitHandler.bind(null, {exit:true}));
process.on('SIGUSR2', exitHandler.bind(null, {exit:true}));
process.on('uncaughtException', exitHandler.bind(null, {exit:true}));

run();
