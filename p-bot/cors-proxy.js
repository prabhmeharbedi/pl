// Simple CORS proxy
const express = require('express');
const cors = require('cors');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const port = 8080;

// Enable CORS for all routes
app.use(cors());

// Proxy middleware configuration
const apiProxy = createProxyMiddleware({
  target: 'https://loopot-835103152018.us-central1.run.app',
  changeOrigin: true,
  pathRewrite: {
    '^/proxy': '' // Remove the '/proxy' path segment when forwarding
  },
  onProxyRes: function(proxyRes, req, res) {
    // Add CORS headers to the response
    proxyRes.headers['Access-Control-Allow-Origin'] = 'https://loopot.vercel.app';
    proxyRes.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS';
    proxyRes.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization';
    proxyRes.headers['Access-Control-Allow-Credentials'] = 'true';
  }
});

// Use the proxy middleware for all requests
app.use('/proxy', apiProxy);

// Start the server
app.listen(port, () => {
  console.log(`CORS Proxy server running at http://localhost:${port}`);
  console.log(`Proxying requests to https://loopot-835103152018.us-central1.run.app`);
  console.log(`You can access the API via http://localhost:${port}/proxy/api/v1/...`);
}); 