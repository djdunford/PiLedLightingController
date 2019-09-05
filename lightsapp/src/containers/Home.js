import React, { Component } from "react";
import { Button } from "react-bootstrap";
import "./Home.css";
import { API } from "aws-amplify";

export default class Home extends Component {

handleRed = async event => {
  event.preventDefault();
  this.setState({ disabled: true });
  const user = await Auth.currentAuthenticatedUser();
  const token = user.signInUserSession.idToken.jwtToken;
  const request = { headers: { Authorization: token } };
  API.get("ledlightingcontroller", "/showsequence/1", request)
      .catch(error => {console.log(error.response)});
};

  render() {
    return (
      <div className="Home">
        <div className="lander">
          <h1>LED Lighting Controller</h1>
          <p>APA102 / SK9822 LED Lighting Controller</p>
        </div>
        <div className="buttons">
          <Button bsStyle="danger" bsSize="large" type="button" onClick={this.handleRed}>RED</Button>
          <Button bsStyle="success" bsSize="large">GREEN</Button>
          <Button bsStyle="primary" bsSize="large">BLUE</Button>
        </div>        
      </div>
    );
  }
}
