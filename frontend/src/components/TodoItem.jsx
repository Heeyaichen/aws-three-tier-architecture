import React from 'react';

const TodoItem = ({ todo, onToggle, onDelete, onEdit }) => {
  const formatDate = (dateString) => {
    if (!dateString) return 'Invalid date';
    try {
      const date = new Date(dateString);
      return isNaN(date) ? 'Invalid date' : date.toLocaleDateString();
    } catch {
      return 'Invalid date';
    }
  };
  
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
          {formatDate(todo.createdAt)}
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