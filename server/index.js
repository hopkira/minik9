const express = require('express');
const bodyParser = require('body-parser');
const pino = require('express-pino-logger')();
const cors = require('cors');

const request = require('request');

var board = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

const issues_opt = {  
    url: 'https://github.ibm.com/api/v3/issues',
    method: 'GET',
    headers: {
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
        'Authorization': 'token 5d48b5c18e1bb2212f1e9369a0dc241aa14885e6',
        'state': 'open',
        'filter': 'assigned'
    }
};

function compare(a,b) {
  const week_a = parseInt(a.number);
  const week_b = parseInt(b.number);
  let comparison = 0;
  if (week_a > week_b){
    comparison = 1
  } else if (week_a < week_b) {
    comparison = -1
  }
  return comparison;
}

const app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(pino);
app.use(bodyParser.json());
app.use(cors());

// receive board FEN string from Python Chess program
app.post('/api/board', (req,res) => {
  board = req.query.board;
  console.log("Board string: " + board);
  var string = JSON.stringify(board);
  res.setHeader('Content-Type', 'application/json');
  res.send('I saw ' + string);
});

// provide FEN string from Python Chess program
// from touch screen front end
app.get('/api/readboard', (req,res) => {
  res.setHeader('Content-Type', 'text/plain;charset=UTF-8');
  res.send(board);
});

// retrive issues from IBM GitHub/ZenHub
app.get('/api/issues', (req, res) => {
    request(issues_opt, function (error, response, body) {
        console.error('Issues error: ', error);
        console.log('Issues status code: ', response && response.statusCode);
        var parsedBody = JSON.parse(body);
        var arrayLength = parsedBody.length;
        var outputArray = [];
        for (var i = 0; i < arrayLength; i++) {
          var issue = parsedBody[i];
          if (issue["milestone"] && issue["milestone"]["title"] !== undefined) {
            var week_num = issue["milestone"]["title"].split(" ")[1]
            var milestone = {number: week_num, title: issue.title};
            outputArray.push(milestone);
          } 
        }
        var string = JSON.stringify(outputArray.sort(compare));
        res.setHeader('Content-Type', 'application/json');
        res.send(string);
        console.log('Issues returned: ', outputArray.length);
      });
});

app.listen(3001, () =>
  console.log('Express server is running on localhost:3001')
);