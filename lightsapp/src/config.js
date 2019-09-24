export default {
  apiGateway: {
    REGION: "eu-west-1",  // TODO remove hardcoded region
    URL: "https://api.debsanddarren.com/lights" // TODO hardcoded API URI
  },
  cognito: {
    REGION: "eu-west-1",  // TODO remove hardcoded region
    USER_POOL_ID: "eu-west-1_gjkbuYvcP",  // TODO remove hardcoded user pool ID
    APP_CLIENT_ID: "6t66amn0i2lgdsgrfg32amd9lh",  // TODO remove hardcoded app client ID
    IDENTITY_POOL_ID: "eu-west-1:97a64b40-c7c3-4357-9e4d-fdc389ada6e9"  // TODO remove hardcoded identity pool ID
  }
};
