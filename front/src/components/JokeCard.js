import React from "react";
import TinderCard from 'react-tinder-card';
import { nl2br } from '../utils/index.js';

const JokeCard = ({ joke, onSwiped, onSwiping, reference }) => {

    return (
        <TinderCard
            className='card-swipe'
            onSwipe={(dir) => onSwiped(dir, joke.id)}
            ref={reference}
            swipeRequirementType='position'
            onSwipeRequirementFulfilled={(dir) => onSwiping(dir)}
            preventSwipe={['up', 'down']}

        >
            <div className='joke-card'>
                <p>{nl2br(joke.content)}</p>
            </div>
        </TinderCard>
    );
}
export default JokeCard;