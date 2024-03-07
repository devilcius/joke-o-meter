import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Container } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';
import { useNavigate } from 'react-router-dom';
import { useFetchJokes } from '../hooks/useFetchJokes';
import { postJokes } from '../api/jokes';
import JokeCard from './JokeCard';
import '../css/JokesCardSwiper.css';

const JokesCardSwiper = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { jokes, session, isFetching } = useFetchJokes();
  const [jokesPayload, setJokesPayload] = useState([]);

  const submitJokes = async () => {
    const response = await postJokes(jokesPayload);
    if (response.status === 201) {
      navigate(`/jokometian/${response.data.uuid}`);
    }
  };

  // Direct DOM manipulation for changing the background color.
  // This approach was chosen due to performance issues encountered with React's context API in this specific scenario.
  // TODO: Investigate alternative state management solutions or optimizations to remove direct DOM manipulation.
  const swiping = (dir) => {
    const appContainer = document.getElementById('jokeometer');
    if (dir === 'left') {
      appContainer.className = 'bg-danger';
    } else if (dir === 'right') {
      appContainer.className = 'bg-success';
    }
  };

  const resetSwiping = () => {
    const appContainer = document.getElementById('jokeometer');
    appContainer.className = '';
  };

  const swiped = async (direction, jokeId) => {
    const joke = { joke: jokeId, liked: direction === 'right', session: session };
    setJokesPayload([...jokesPayload, joke]);
    resetSwiping(); // Reset swipe effect
    if (jokesPayload.length + 1 === jokes.length) {
      await new Promise(resolve => setTimeout(resolve, 1000));
      await submitJokes();
    }
  };

  if (isFetching) {
    return <div>{t('swiper.loading')}</div>;
  }

  return (
    <>
      <Container className='mt-4 card-bootstrap-container'>
        {(jokes.length === jokesPayload.length) && (
          <div className="no-more-cards text-center">
            <h2>{t('swiper.no_more_cards')}</h2>
            <div><small>{t('swiper.generating_character')}</small></div>
            <div className="mt-2"><FontAwesomeIcon icon={faSpinner} spin size="2x" /></div>
          </div>
        )}
        <h5 className="text-info">{`${t('swiper.remaining_cards', { 'count': jokes.length - jokesPayload.length })} `}</h5>
        <div id="card-swiper-container" >
          <div className='card-container'>
            {jokes.map((joke, index) => (
              <JokeCard
                key={joke.id}
                joke={joke}
                onSwiped={(dir) => swiped(dir, joke.id)}
                onSwiping={(dir) => swiping(dir)}
              />
            ))}
          </div>
        </div>
      </Container>
    </>
  );
};

export default JokesCardSwiper;
