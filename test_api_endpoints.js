/**
 * Test REST API Endpoints
 * Checks if API endpoints are working and if frontend can fetch from them
 */

const http = require('http');

const API_BASE = 'http://localhost:3000';

function makeRequest(method, path, data = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, API_BASE);
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    };

    const req = http.request(url, options, (res) => {
      let body = '';
      res.on('data', (chunk) => {
        body += chunk;
      });
      res.on('end', () => {
        try {
          const isJson = res.headers['content-type']?.includes('application/json');
          resolve({
            status: res.statusCode,
            headers: res.headers,
            body: isJson ? JSON.parse(body) : body.substring(0, 200),
            isJson,
          });
        } catch (e) {
          resolve({
            status: res.statusCode,
            headers: res.headers,
            body: body.substring(0, 200),
            isJson: false,
          });
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    if (data) {
      req.write(JSON.stringify(data));
    }

    req.end();
  });
}

async function testEndpoints() {
  console.log('Testing REST API Endpoints');
  console.log('==========================\n');

  const tests = [
    {
      name: 'GET /api/patients',
      method: 'GET',
      path: '/api/patients',
    },
    {
      name: 'GET /api/patients?keyword=test',
      method: 'GET',
      path: '/api/patients?keyword=test',
    },
    {
      name: 'GET /api/patients/1',
      method: 'GET',
      path: '/api/patients/1',
    },
    {
      name: 'POST /api/patients',
      method: 'POST',
      path: '/api/patients',
      data: {
        pname: 'Test Patient',
        pbirth: '1990-01-01',
        sex: 'M',
      },
    },
    {
      name: 'GET /api/cards',
      method: 'GET',
      path: '/api/cards',
    },
    {
      name: 'GET /api/payments/history/1',
      method: 'GET',
      path: '/api/payments/history/1',
    },
  ];

  const results = [];

  for (const test of tests) {
    try {
      console.log(`Testing: ${test.name}...`);
      const result = await makeRequest(test.method, test.path, test.data);
      
      const status = result.status;
      const isSuccess = status >= 200 && status < 300;
      const isError = status >= 400;
      const is404 = status === 404;
      
      let statusIcon = '✅';
      if (is404) statusIcon = '❌';
      else if (isError) statusIcon = '⚠️';
      else if (!isSuccess) statusIcon = '❓';

      console.log(`  ${statusIcon} Status: ${status}`);
      
      if (result.isJson) {
        if (result.body.message) {
          console.log(`  Message: ${result.body.message}`);
        }
        if (result.body.patients) {
          console.log(`  Patients found: ${result.body.patients.length}`);
        }
        if (result.body.error) {
          console.log(`  Error: ${result.body.error}`);
        }
      } else {
        if (result.body.includes('404')) {
          console.log(`  ⚠️  Route not found (404)`);
        } else if (result.body.includes('error')) {
          console.log(`  ⚠️  Error in response`);
        }
      }

      results.push({
        ...test,
        status,
        success: isSuccess && !is404,
        is404,
      });

      console.log('');
    } catch (error) {
      console.log(`  ❌ Error: ${error.message}\n`);
      results.push({
        ...test,
        status: 0,
        success: false,
        error: error.message,
      });
    }
  }

  // Summary
  console.log('\n=== Summary ===');
  const successful = results.filter(r => r.success).length;
  const failed = results.filter(r => !r.success && !r.is404).length;
  const notFound = results.filter(r => r.is404).length;

  console.log(`✅ Working: ${successful}`);
  console.log(`❌ Not Found (404): ${notFound}`);
  console.log(`⚠️  Errors: ${failed}`);

  if (notFound > 0) {
    console.log('\n⚠️  API routes are returning 404. Possible issues:');
    console.log('   1. Next.js API routes not properly configured');
    console.log('   2. Server needs to be restarted');
    console.log('   3. Routes might be in wrong location');
    console.log('   4. Database connection error causing route failure');
  }

  if (successful > 0) {
    console.log('\n✅ Some endpoints are working!');
  }

  return results;
}

// Run tests
testEndpoints()
  .then(() => {
    console.log('\n=== Frontend API Client Check ===');
    console.log('Frontend uses: lib/api-client.ts');
    console.log('API calls use relative paths: /api/...');
    console.log('This means frontend will call: http://localhost:3000/api/...');
    console.log('\nIf API endpoints return 404, frontend will receive errors.');
    console.log('Check browser console for fetch errors when using the UI.');
  })
  .catch(console.error);

