// モジュールのロード
const http = require('http');
const fs = require('fs');
const mime = {
  ".html": "text/html",
  ".css": "text/css"
  // 読み取りたいMIMEタイプはここに追記
};

// サーバーオブジェクトの作成
var server = http.createServer();

server.on('request', function (req, res) {
  console.log(req.url)
  var target = ''
  switch (req.url) {
    case '/index.css':
      target = 'index.css';
      var mine = "text/css"
      break
    default:
      target = 'index.html';
      var mine = "text/html"
      break
  }
  fs.readFile(target, 'UTF-8',
    (error, data) => {
      // エラー処理
      if (error) {
        response.writeHead(500, { "Content-Type": mine });
        response.write("500 Internal Server Error\n");
        res.end();
      }

      res.writeHead(200, { 'Content-Type': mine });
      res.write(data);
      res.end();
    });
});

// 待ち受け開始
server.listen(8080);
console.log('Server running');
