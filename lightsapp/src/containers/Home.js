import React, { Component } from "react";
import { Button } from "react-bootstrap";
import "./Home.css";

export default class Home extends Component {
  render() {
    return (
      <div className="Home">
        <div className="lander">
          <h1>LED Lighting Controller</h1>
          <p>APA102 / SK9822 LED Lighting Controller</p>
        </div>
        <div className="buttons">
          <Button bsStyle="danger" bsSize="large">RED</Button>
          <Button bsStyle="success" bsSize="large">GREEN</Button>
          <Button bsStyle="primary" bsSize="large">BLUE</Button>
        </div>        
      </div>
    );
  }
}
