import React from 'react';
import { Button } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import '../css/WelcomePage.css';
import { Link } from 'react-router-dom';

const WelcomePage = () => {
    const { t } = useTranslation();

    return (
        <div className="welcome-page" >
            <h1 className="text-center"><strong>{t('welcome.lead')}</strong></h1>
            <img className="background-image" src="/pure_soul_jokometian.svg" alt="background logo" />
            <div className="play-button-container">
                <Button variant="primary" className="play-button" size="lg" href="#play" as={Link} to="/swipe">
                    {t('welcome.play')}
                </Button>
            </div>
        </div>
    );
};

export default WelcomePage;