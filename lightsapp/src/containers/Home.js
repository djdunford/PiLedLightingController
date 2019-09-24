import React, { Component } from "react";
import { Button } from "react-bootstrap";
import "./Home.css";
import { API } from "aws-amplify";

export default class Home extends Component {

    handleRed = async event => {
        event.preventDefault();
        API.get("ledlightingcontroller", "/showsequence/1")
            .catch(error => {console.log(error.response)});
    };

    handleGreen = async event => {
        event.preventDefault();
        API.get("ledlightingcontroller", "/showsequence/2")
            .catch(error => {console.log(error.response)});
    };

    handleBlue = async event => {
        event.preventDefault();
        API.get("ledlightingcontroller", "/showsequence/3")
            .catch(error => {console.log(error.response)});
    };

    handleOff = async event => {
        event.preventDefault();
        API.get("ledlightingcontroller", "/off")
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
                    <Button bsStyle="success" bsSize="large" type="button" onClick={this.handleGreen}>GREEN</Button>
                    <Button bsStyle="primary" bsSize="large" type="button" onClick={this.handleBlue}>BLUE</Button>
                    <Button bsStyle="primary" bsSize="large" type="button" onClick={this.handleOff}>OFF</Button>
                </div>
            </div>
        );
    }
}
