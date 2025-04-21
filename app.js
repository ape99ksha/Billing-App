import { supabase } from '../lib/supabase';
import { useState, useEffect } from 'react';

function MyApp({ Component, pageProps }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Check active session on load
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user || null);
    });

    // Listen for auth changes (login/logout)
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      setUser(session?.user || null);
    });

    return () => subscription.unsubscribe();
  }, []);

  return <Component {...pageProps} user={user} />;
}

export default MyApp;
