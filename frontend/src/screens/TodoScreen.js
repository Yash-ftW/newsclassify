import { useState } from "react";
import TodoDisplay from "../components/TodoComponent/TodoDisplay";
import TodoInput from "../components/TodoComponent/TodoInput";

const TodoScreen = () => {
  const [value, setValue] = useState([]);

  const inputHandler = (val) => {
    setValue((prevState) => {
      return [val, ...prevState];
    });
  };

  const inputDeleter = (index) => {
    setValue(
      value.filter((arg, id) => {
        return id !== index;
      })
    );
  };

  return (
    <div>
      <h3 className="todo-title">To-Do</h3>
      <TodoInput onInputHandler={inputHandler} />
      <TodoDisplay sendTask={value} onDelete={inputDeleter} />
    </div>
  );
};

export default TodoScreen;
