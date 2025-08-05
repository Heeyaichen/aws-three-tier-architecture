import React, { useState, useEffect } from 'react';

const TodoForm = ({ onSubmit, editingTodo, onCancel }) => {
  const [text, setText] = useState('');

  useEffect(() => {
    if (editingTodo) {
      setText(editingTodo.text);
    } else {
      setText('');
    }
  }, [editingTodo]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) {
      if (editingTodo) {
        onSubmit(editingTodo.id, text.trim());
      } else {
        onSubmit(text.trim());
      }
      setText('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="todo-form">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={editingTodo ? "Edit todo..." : "Add a new todo..."}
        className="todo-input"
        autoFocus
      />
      <div className="form-buttons">
        <button type="submit" className="submit-btn">
          {editingTodo ? 'Update' : 'Add'}
        </button>
        {editingTodo && (
          <button type="button" onClick={onCancel} className="cancel-btn">
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};

export default TodoForm;