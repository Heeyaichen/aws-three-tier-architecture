import React from 'react';

const TodoItem = ({ todo, onToggle, onDelete, onEdit }) => {
  const isValidDate = todo.createdAt && !isNaN(new Date(todo.createdAt));
  
  return (
    <div className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <div className="todo-content">
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={() => onToggle(todo.id)}
          className="todo-checkbox"
          aria-label={`Mark ${todo.text} as ${todo.completed ? 'incomplete' : 'complete'}`}
        />
        <span className="todo-text">{todo.text}</span>
        <span className="todo-date">
          {isValidDate ? new Date(todo.createdAt).toLocaleDateString() : 'Invalid date'}
        </span>
      </div>
      <div className="todo-actions">
        <button
          onClick={() => onEdit(todo)}
          className="edit-btn"
          disabled={todo.completed}
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(todo.id)}
          className="delete-btn"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TodoItem;