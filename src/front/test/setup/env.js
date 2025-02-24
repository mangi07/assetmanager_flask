// env.js
const fs = require('fs');
const path = require('path');

function loadEnv() {
  const envFilePath = path.resolve(__dirname, '.env');
  
  if (fs.existsSync(envFilePath)) {
    const envFileContent = fs.readFileSync(envFilePath, 'utf-8');
    const lines = envFileContent.split('\n');

    lines.forEach(line => {
      if (line && !line.startsWith('#')) {
        const [key, value] = line.split('=');
        if (key && value) {
          process.env[key.trim()] = value.trim();
        }
      }
    });
  }
}

loadEnv()

var env = {
  "username": process.env.USERNAME,
  "password": process.env.PASSWORD,
};

export { env };

