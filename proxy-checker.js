#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function askForFile() {
  rl.question('📝 Nhập tên file proxy (VD: proxy.txt): ', (filename) => {
    const filePath = path.join(process.cwd(), filename);
    
    if (!fs.existsSync(filePath)) {
      console.error(`❌ File không tìm thấy: ${filePath}`);
      rl.close();
      process.exit(1);
    }

    const proxies = fs
      .readFileSync(filePath, 'utf-8')
      .split('\n')
      .map(line => line.trim())
      .filter(line => line && line.match(/^\d+\.\d+\.\d+\.\d+:\d+$/));

    console.log(`\n✅ Tìm thấy ${proxies.length} proxy\n`);
    console.log('⏳ Bắt đầu kiểm tra...\n');

    const workingProxies = [];
    const failedProxies = [];
    let completed = 0;

    proxies.forEach((proxy, index) => {
      setTimeout(() => {
        checkProxy(proxy, (isWorking) => {
          completed++;
          const status = isWorking ? '✅' : '❌';
          console.log(`[${completed}/${proxies.length}] ${status} ${proxy}`);

          if (isWorking) {
            workingProxies.push(proxy);
          } else {
            failedProxies.push(proxy);
          }

          if (completed === proxies.length) {
            displayResults(workingProxies, failedProxies, filename);
          }
        });
      }, index * 100);
    });
  });
}

function checkProxy(proxy, callback) {
  const [ip, port] = proxy.split(':');
  const timeout = 5000;

  const agent = new http.Agent({
    httpVersion: '1.1',
    keepAlive: false,
    family: 4
  });

  const options = {
    hostname: 'httpbin.org',
    port: 80,
    path: '/ip',
    method: 'GET',
    agent: agent,
    timeout: timeout,
    headers: {
      'User-Agent': 'Mozilla/5.0'
    }
  };

  const req = http.request(options, (res) => {
    res.on('data', () => {});
    res.on('end', () => {
      callback(res.statusCode === 200);
    });
  });

  req.on('error', () => {
    callback(false);
  });

  req.on('timeout', () => {
    req.destroy();
    callback(false);
  });

  req.end();
}

function displayResults(working, failed, filename) {
  console.log('\n' + '='.repeat(60));
  console.log('📊 KẾT QUẢ KIỂM TRA');
  console.log('='.repeat(60));
  console.log(`✅ Proxy hoạt động: ${working.length}`);
  console.log(`❌ Proxy lỗi: ${failed.length}`);
  console.log(`📈 Tỉ lệ: ${((working.length / (working.length + failed.length)) * 100).toFixed(2)}%`);
  console.log('='.repeat(60) + '\n');

  if (working.length > 0) {
    const workingFile = filename.replace(/\.(txt|lst|list)$/i, '_working.txt');
    fs.writeFileSync(workingFile, working.join('\n'));
    console.log(`💾 Proxy hoạt động đã lưu: ${workingFile}`);
  }

  console.log('\n✨ Hoàn tất kiểm tra!');
  rl.close();
  process.exit(0);
}

console.log('╔════════════════════════════════════════╗');
console.log('║     🔍 PROXY CHECKER TOOL 🔍          ║');
console.log('║  Kiểm tra proxy từ file .txt          ║');
console.log('╚════════════════════════════════════════╝\n');

askForFile();
