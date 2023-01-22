import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import FormContainer from "../components/FormContainer";

function LoginScreen() {
  const [id, setId] = useState("");
  const [password, setPassword] = useState("");

  const submitHandler = (e) => {
    e.preventDefault();
    alert("Submit");
  };
  return (
    <FormContainer>
      <h1>Sign In</h1>

      <Form onSubmit={submitHandler}>
        <Form.Group controlId="email">
          <Form.Label>Student ID</Form.Label>
          <Form.Control
            type="number"
            placeholder="Enter Student ID"
            val={id}
            onChange={(e) => setId(e.target.value)}
          ></Form.Control>
        </Form.Group>

        <Form.Group controlId="password">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Enter Password"
            val={password}
            onChange={(e) => setPassword(e.target.value)}
          ></Form.Control>
        </Form.Group>
        <br />
        <Button type="submit" variant="primary">
          Sign In
        </Button>
      </Form>
    </FormContainer>
  );
}

export default LoginScreen;
