/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: "http://127.0.0.1:5000", // the running FLASK api server url
  auth0: {
    url: "zoran-01.us", // the auth0 domain prefix
    audience: "dev", // the audience set for the auth0 app
    clientId: "yUwkWHrQxtgXQ3R9Dcknyi22Cr4QaZIo", // the client id generated for the auth0 app
    callbackURL: "https://localhost:8100/login-results", // the base url of the running ionic application.
  },
};
