const { mongoClient } = require('../mongoConnector');
const db = mongoClient.db('reactsampledb');

module.exports = {
  setData: async (req, res) => {
    try {
      const mBody = req.body;
      const mPath = mBody.path;
      const mData = mBody.data;
      mData['_id'] = mPath;
      const dataCollection = db.collection('data');
      await dataCollection.insertOne(mData);
      res.status(201).json('ok');
    } catch (err) {
      if (err.code == 11000) {
        res.status(400).json('already existed');
      } else throw err;
    }
  },
  
  getData: async (req, res) => {
    try {
      const mBody = req.body;
      const mPath = mBody.path;
      console.log(mPath);
      const dataCollection = db.collection('data');
      const selector = { "_id": { $regex: mPath, $options:"i" } };
      const mData = await dataCollection.find(selector).toArray();
      //console.log(mData);
      if (mData != null) {
        // delete mData['_id'];
        res.status(200).json(mData);
      } else {
        console.log('here');
        res.status(200).json(mData);
      }
    } catch (err) {
      console.log(err);
      res.status(400).json('error');
    }
  },

  updateData: async (req, res) => {
    const mBody = req.body;
    const mPath = mBody.path;
    const mData = mBody.data;
    const updateDoc = {
      $set: mData
    };
    const dataCollection = db.collection(mPath);
    try {
      await dataCollection.updateOne({}, updateDoc);
      res.status(200).json('ok');
    } catch (e) {
      res.status(404).json('wrong');
    }
  },
};
