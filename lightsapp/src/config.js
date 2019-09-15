export default {
  apiGateway: {
    REGION: "eu-west-1",  // TODO remove hardcoded region
    URL: "https://api.debsanddarren.com/lights" // TODO hardcoded API URI
  },
  cognito: {
    REGION: "eu-west-1",  // TODO remove hardcoded region
    USER_POOL_ID: "eu-west-1_L7Ck7fcxb",  // TODO remove hardcoded user pool ID
    APP_CLIENT_ID: "4jdl5geaahich5idjs0c52o200",  // TODO remove hardcoded app client ID
    IDENTITY_POOL_ID: "eu-west-1:ee092402-95fa-474e-bbfc-340ab7535da8"  // TODO remove hardcoded identity pool ID
  }
};
