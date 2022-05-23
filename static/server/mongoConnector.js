const { MongoClient, ServerApiVersion } = require('mongodb');
const mongoCreds = require('./secrets/mongocreds.js');
const client = new MongoClient(mongoCreds, { useNewUrlParser: true, useUnifiedTopology: true, serverApi: ServerApiVersion.v1 });

async function connect() {
  const mPromise = await client.connect();
  return mPromise;
}

module.exports = {
  connect: connect,
  mongoClient: client
};
