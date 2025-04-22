import { supabase } from '../lib/supabase';
import { useState, useEffect } from 'react';

export default function Home() {
  const [todos, setTodos] = useState([]);

  // Fetch todos from Supabase
  useEffect(() => {
    const fetchTodos = async () => {
      const { data } = await supabase.from('todos').select('*');
      setTodos(data);
    };
    fetchTodos();
  }, []);

  return (
    <div>
      <h1>Todos</h1>
      {todos.map((todo) => (
        <p key={todo.id}>{todo.task}</p>
      ))}
    </div>
  );
}
