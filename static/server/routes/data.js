const express = require('express');
const { setData, updateData, getData }  = require('../controllers/data');

const router = express.Router();

router.post('/', setData);
router.put('/', updateData);
router.post('/get', getData);

module.exports = router;
