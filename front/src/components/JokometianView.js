import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import '../css/JokometianView.css';
import { fetchJokometian } from '../api/jokometians';
import { useTranslation } from 'react-i18next';
import { Card } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckCircle } from '@fortawesome/free-solid-svg-icons';
import Toast from 'react-bootstrap/Toast';
import JokometianTraits from './JokometianTraits';
import JokometianAmmunition from './JokometianAmmunition';
import JokometianArsenal from './JokometianArsenal'; 
import CopyUrl from './CopyUrl';
import i18n from '../i18n';

const JokometianView = () => {
    const { t } = useTranslation();
    const { id } = useParams();
    const [jokometian, setJokometian] = useState({});
    const [showToast, setShowToast] = React.useState(false);
    const [flipped, setFlipped] = useState(false); // New state to manage flip
    const currentLanguage = i18n.language;
    const toastCopiedMessage = t('toast.copy_url_success');
    useEffect(() => {
        const fetchJokometianData = async () => {
            const response = await fetchJokometian(id);
            if (response.status === 200) {
                setJokometian(response.data);
            }
        };
        fetchJokometianData();
    }, [id, currentLanguage]);

    const handleFlip = () => {
        setFlipped(!flipped); // Toggle the flipped state
    };

    if (Object.keys(jokometian).length === 0) {
        return <div>{t('jokometian.loading')}</div>;
    }
    const onToastClose = (e) => {
        // sanity check, it could be called on autohide
        console.log("e", e);
        if (e) {
            e.stopPropagation();
        }
        setShowToast(false);
    }

    // Build jokeometian URL from jokematian id
    const jokometianUrl = `${window.location.origin}/jokometian/${jokometian.id}`;

    return (
        <>
            <Toast
                className="copy-toast-container"
                show={showToast}
                onClose={onToastClose}
                delay={5000}
                autohide
                position='bottom-end'
            >
                <Toast.Header>
                    <div className='d-flex gap-2'>
                        <FontAwesomeIcon className='align-self-center' icon={faCheckCircle} color='green' />
                        <strong className="mr-auto">{t('toast.success')}</strong>
                    </div>
                </Toast.Header>
                <Toast.Body className="toast-body">{toastCopiedMessage}</Toast.Body>
            </Toast>

            <div className="d-flex align-items-center justify-content-center jokometian-view-container">
                <div className={`flip-card ${flipped ? 'flipped' : ''}`} onClick={handleFlip}>
                    <div className="flip-card-inner">
                        <div className="flip-card-front">
                            <Card style={{ width: '23rem' }} className='shadow-lg p-3 mb-5 bg-white rounded'>
                                <Card.Header className="d-flex justify-content-between">{t('jokometian.title')}
                                    <CopyUrl url={jokometianUrl} currentLanguage={i18n.language} textCopied={() => setShowToast(true)} />
                                </Card.Header>
                                <Card.Img variant="top" src={jokometian.image_url} />
                                <Card.Body>
                                    <Card.Title>{jokometian.name}</Card.Title>
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
        </>
    );
}

export default JokometianView;
