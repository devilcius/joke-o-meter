// hooks/useFetchJokes.js
import { useState, useEffect } from 'react';
import { fetchJokes } from '../api/jokes';
import i18n from '../i18n';

export const useFetchJokes = () => {
  const [jokes, setJokes] = useState([]);
  const [session, setSession] = useState(null);
  const [isFetching, setIsFetching] = useState(true);
  const currentLanguage = i18n.language;
  useEffect(() => {
    const fetchJokesData = async () => {
      try {
        const response = await fetchJokes();
        if (response.status === 200) {
          setJokes(response.data.jokes);
          setSession(response.data.session);
        } else {
          // Handle non-200 responses if necessary
        }
      } catch (error) {
        console.error('Failed to fetch jokes:', error);
        // Handle errors, such as by setting an error state (not shown here)
      } finally {
        setIsFetching(false);
      }
    };
    fetchJokesData();
  }, [currentLanguage]);

  return { jokes, session, isFetching };
}
