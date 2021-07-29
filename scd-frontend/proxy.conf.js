
const PROXY_CONFIG = {
  "/api": {
      target: `http://localhost:3004/`,
      "secure": "false",
      "logLevel": "debug",
  },
};

module.exports = PROXY_CONFIG;