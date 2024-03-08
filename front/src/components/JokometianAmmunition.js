import React from "react";
import { useTranslation } from 'react-i18next';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRocket } from '@fortawesome/free-solid-svg-icons';
import { Row } from 'react-bootstrap';
import { Col } from 'react-bootstrap';

const JokometianAmmunition = ({ numberOfAmmunitions }) => {
    const { t } = useTranslation();
    let ammunition = [];
    for (let i = 0; i < numberOfAmmunitions; i++) {
        ammunition.push(<span key={i}><FontAwesomeIcon icon={faRocket} /></span>);
    }

    return (
        <Row className="jokometian-ammunition">
            <Col xs={3}>
                {t('jokometian.arsenal')}:
            </Col>
            <Col xs={9}>
                {ammunition}
            </Col>
        </Row>
    );
}

export default JokometianAmmunition;