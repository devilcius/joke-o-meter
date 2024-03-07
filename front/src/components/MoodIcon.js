import React from 'react';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSmile } from '@fortawesome/free-solid-svg-icons';
import { faFrown } from '@fortawesome/free-solid-svg-icons';

const MoodIcon = ({ mood, display: displayIcon }) => {

    const moodIcon = mood === 'happy' ? faSmile : faFrown;

    const moodIconStyle = {
        color: 'white',
        top: '2%',
        right: '2%',
        position: 'absolute',
    }

    return (
        <span style={moodIconStyle}>
            <FontAwesomeIcon display={displayIcon} icon={moodIcon} size="2x" />
        </span>
    )
}

export default MoodIcon;