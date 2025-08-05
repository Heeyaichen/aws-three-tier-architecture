# Todo App - React CRUD Application

A simple, modern Todo application built with React and Vite that demonstrates full CRUD (Create, Read, Update, Delete) functionality.

## Features

- ✅ **Create** - Add new todos with a clean form interface
- ✅ **Read** - View all todos with completion status and creation date
- ✅ **Update** - Edit existing todos inline
- ✅ **Delete** - Remove individual todos or clear all completed ones
- ✅ **Toggle Completion** - Mark todos as complete/incomplete
- ✅ **Local Storage** - Persist todos between browser sessions
- ✅ **Statistics** - View total, completed, and remaining todo counts
- ✅ **Responsive Design** - Works on desktop and mobile devices

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open your browser and navigate to the local development URL

## Project Structure

```
src/
├── components/
│   ├── TodoForm.jsx    # Form for adding/editing todos
│   ├── TodoList.jsx    # Container for all todos
│   ├── TodoItem.jsx    # Individual todo item
│   └── Navbar.jsx      # Simple header component
├── App.jsx             # Main application component
├── App.css             # Application styles
└── main.jsx            # Application entry point
```

## CRUD Operations

- **Create**: Use the input form at the top to add new todos
- **Read**: All todos are displayed in a list with their status and creation date
- **Update**: Click the "Edit" button on any todo to modify its text
- **Delete**: Click the "Delete" button to remove individual todos, or "Clear Completed" to remove all finished tasks

## Technologies Used

- React 19.1.0
- Vite (for fast development and building)
- Modern CSS with Flexbox and Grid
- Local Storage API for data persistence
