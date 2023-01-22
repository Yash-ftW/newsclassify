import "./TodoDisplay.css";

const TodoDisplay = (props) => {
  return (
    <div>
      {props.sendTask.map((arg, index) => (
        <div className="Todo-display">
          <div className="Todo-task">{arg}</div>
          <button
            className="Todo-delete"
            onClick={() => {
              props.onDelete(index);
            }}
          >
            Delete
          </button>
        </div>
      ))}
    </div>
  );
};

export default TodoDisplay;
