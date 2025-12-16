/**
 * Remote REST API Connection Check
 * Tests connection to the remote REST API service
 */

const http = require('http');

const API_BASE_URL = process.env.API_BASE_URL || process.env.REMOTE_API_URL || 'http://localhost:3000';

function makeRequest(method, path) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, API_BASE_URL);
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      timeout: 5000,
    };

    const req = http.request(url, options, (res) => {
      let body = '';
      res.on('data', (chunk) => {
        body += chunk;
      });
      res.on('end', () => {
        resolve({
          status: res.statusCode,
          headers: res.headers,
          body: body.substring(0, 200),
        });
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });

    req.end();
  });
}

async function checkRemoteAPI() {
  console.log('Remote REST API Connection Check');
  console.log('=================================\n');
  
  console.log(`API Base URL: ${API_BASE_URL}\n`);

  const tests = [
    { name: 'GET /api/patients', method: 'GET', path: '/api/patients' },
    { name: 'GET /api/patients?keyword=test', method: 'GET', path: '/api/patients?keyword=test' },
  ];

  let successCount = 0;
  let errorCount = 0;

  for (const test of tests) {
    try {
      console.log(`Testing: ${test.name}...`);
      const result = await makeRequest(test.method, test.path);
      
      if (result.status === 200 || result.status === 404) {
        // 200 = success, 404 = endpoint exists but may need data
        console.log(`  ✅ Status: ${result.status}`);
        if (result.status === 200) {
          successCount++;
        }
      } else {
        console.log(`  ⚠️  Status: ${result.status}`);
        errorCount++;
      }
    } catch (error) {
      console.log(`  ❌ Error: ${error.message}`);
      errorCount++;
    }
    console.log('');
  }

  console.log('=== Summary ===');
  console.log(`✅ Successful: ${successCount}`);
  console.log(`⚠️  Errors: ${errorCount}`);
  
  if (errorCount === 0 && successCount > 0) {
    console.log('\n✅ Remote API is accessible and working!');
  } else if (errorCount > 0) {
    console.log('\n⚠️  Remote API connection issues detected.');
    console.log('   Please check:');
    console.log(`   1. Remote API service is running at ${API_BASE_URL}`);
    console.log('   2. API_BASE_URL environment variable is correct');
    console.log('   3. Network connectivity');
  } else {
    console.log('\n⚠️  Remote API is accessible but endpoints may need configuration.');
  }
}

checkRemoteAPI().catch(console.error);

