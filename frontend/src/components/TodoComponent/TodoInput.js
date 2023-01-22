import { useState } from "react";
import "./TodoInput.css";

const TodoInput = (props) => {
  const [input, setInput] = useState("");
  const valHandler = (event) => {
    return setInput(event.target.value);
  };

  const valKeeper = (e) => {
    e.preventDefault();
    props.onInputHandler(input);
    setInput("");
  };

  return (
    <form onSubmit={valKeeper}>
      <div className="Todo-container">
        <input
          className="Todo-input"
          placeholder="Enter Tasks..."
          onChange={valHandler}
          value={input}
        />
        <button className="Todo-button" type="submit">
          Add Task
        </button>
      </div>
    </form>
  );
};

export default TodoInput;
