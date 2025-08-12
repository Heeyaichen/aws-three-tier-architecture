import React, { useState, useEffect } from 'react';
import TodoForm from './components/TodoForm';
import TodoList from './components/TodoList';
import './App.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000';

function App() {
  const [todos, setTodos] = useState([]);
  const [editingTodo, setEditingTodo] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/todos`);
      const data = await response.json();
      setTodos(data);
    } catch (error) {
      console.error('Error fetching todos:', error);
    }
    setLoading(false);
  };

  const addTodo = async (text) => {
    try {
      const response = await fetch(`${API_BASE_URL}/todos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      const newTodo = await response.json();
      setTodos(prev => [...prev, newTodo]);
    } catch (error) {
      console.error('Error adding todo:', error);
    }
  };

  const updateTodo = async (id, text) => {
    try {
      const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      const updatedTodo = await response.json();
      setTodos(prev => prev.map(todo => todo.id === id ? updatedTodo : todo));
      setEditingTodo(null);
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await fetch(`${API_BASE_URL}/todos/${id}`, { method: 'DELETE' });
      setTodos(prev => prev.filter(todo => todo.id !== id));
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  const toggleComplete = async (id) => {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;
    try {
      const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !todo.completed })
      });
      const updatedTodo = await response.json();
      setTodos(prev => prev.map(t => t.id === id ? updatedTodo : t));
    } catch (error) {
      console.error('Error toggling todo:', error);
    }
  };

  const clearCompleted = async () => {
    const completedTodos = todos.filter(todo => todo.completed);
    try {
      await Promise.all(
        completedTodos.map(todo => 
          fetch(`${API_BASE_URL}/todos/${todo.id}`, { method: 'DELETE' })
        )
      );
      setTodos(todos.filter(todo => !todo.completed));
    } catch (error) {
      console.error('Error clearing completed todos:', error);
    }
  };

  const completedCount = todos.filter(todo => todo.completed).length;
  const totalCount = todos.length;

  return (
    <div className="App">
      <header className="app-header">
        <h1>To-Do App</h1>
        <p>Three-Tier Architecture with AWS</p>
      </header>
      
      <main className="app-main">
        <div className="todo-container">
          {loading && <div className="loading">Loading...</div>}
          
          <TodoForm 
            onSubmit={editingTodo ? updateTodo : addTodo}
            editingTodo={editingTodo}
            onCancel={() => setEditingTodo(null)}
          />
          
          <div className="todo-stats">
            <span>Total: {totalCount}</span>
            <span>Completed: {completedCount}</span>
            <span>Remaining: {totalCount - completedCount}</span>
            {completedCount > 0 && (
              <button onClick={clearCompleted} className="clear-btn">
                Clear Completed
              </button>
            )}
          </div>
          
          <TodoList 
            todos={todos}
            onToggle={toggleComplete}
            onDelete={deleteTodo}
            onEdit={setEditingTodo}
          />
        </div>
      </main>
    </div>
  );
}

export default App;
