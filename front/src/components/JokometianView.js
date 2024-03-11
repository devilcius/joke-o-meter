import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import '../css/JokometianView.css'; // Ensure your CSS file is correctly imported
import { fetchJokometian } from '../api/jokometians';
import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet';
import { Card } from 'react-bootstrap';
import JokometianTraits from './JokometianTraits';
import JokometianAmmunition from './JokometianAmmunition';
import JokometianArsenal from './JokometianArsenal'; // Import the JokometianJokes component
import { getJokometianTraitMapper } from '../utils/index';
import CopyUrl from './CopyUrl';

const JokometianView = () => {
    const { t } = useTranslation();
    const TRAITS_MAPPER = getJokometianTraitMapper(t);
    const { id } = useParams();
    const [jokometian, setJokometian] = useState({});
    const [flipped, setFlipped] = useState(false); // New state to manage flip

    useEffect(() => {
        const fetchJokometianData = async () => {
            const response = await fetchJokometian(id);
            if (response.status === 200) {
                setJokometian(response.data);
            }
        };
        fetchJokometianData();
    }, [id]);

    const handleFlip = () => {
        setFlipped(!flipped); // Toggle the flipped state
    };

    if (Object.keys(jokometian).length === 0) {
        return <div>{t('jokometian.loading')}</div>;
    }
    // Build jokeometian URL from jokematian id
    const jokometianUrl = `${window.location.origin}/jokometian/${jokometian.id}`;
    const jokometianImageUrl = `${window.location.origin}${jokometian.image_url}`;    

    return (
        <div className="d-flex align-items-center justify-content-center jokometian-view-container">
            <Helmet>
                <title>Joke-O-Meter: {TRAITS_MAPPER[jokometian.name].name}</title>
                <meta property="og:title" content={TRAITS_MAPPER[jokometian.name].name} />
                <meta property="og:description" content={jokometian.description} />
                <meta property="og:image" content={jokometianImageUrl} />
                <meta property="og:url" content={jokometianUrl} />
            </Helmet>
            <div className={`flip-card ${flipped ? 'flipped' : ''}`} onClick={handleFlip}>
                <div className="flip-card-inner">
                    <div className="flip-card-front">
                        <Card style={{ width: '23rem' }} className='shadow-lg p-3 mb-5 bg-white rounded'>
                            <Card.Header className="d-flex justify-content-between">{t('jokometian.title')}<CopyUrl url={jokometianUrl} /></Card.Header>
                            <Card.Img variant="top" src={jokometian.image_url} />
                            <Card.Body>
                                <Card.Title>{TRAITS_MAPPER[jokometian.name].name}</Card.Title>
                                <div>
                                    {jokometian.description}
                                    <hr />
                                    <JokometianTraits traits={jokometian.traits} />
                                    <hr />
                                    <JokometianAmmunition numberOfAmmunitions={jokometian.jokes?.length} />
                                </div>
                            </Card.Body>
                        </Card>
                    </div>
                    <div className="flip-card-back">
                        <Card className='jokes-arsenal shadow-lg p-3 mb-5 bg-white rounded'>
                            <Card.Header>{t('jokometian.jokes')}</Card.Header>
                            <Card.Body>
                                {/* Render the JokometianJokes component with jokometian data */}
                                <JokometianArsenal jokometian={jokometian} />
                            </Card.Body>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default JokometianView;
