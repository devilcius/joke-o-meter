import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSmileBeam, faFrownOpen, faHandPointer } from '@fortawesome/free-solid-svg-icons';
import { useTranslation } from 'react-i18next';
import '../css/Instructions.css';

const Instructions = () => {
    const { t } = useTranslation();
    return (
        <Container className="text-center my-4">
            <h1>{t('instructions.title')}</h1>
            <Row className="align-items-center my-3">
                <Col >
                    <FontAwesomeIcon icon={faFrownOpen} size="3x" color="red" />
                </Col>
                <Col>
                    <FontAwesomeIcon icon={faSmileBeam} size="3x" color="green" />
                </Col>
            </Row>
            <Row lg="10" className='align-items-center my-3'>
                <Col>
                    <FontAwesomeIcon icon={faHandPointer} size="3x" className="swipe-animation" />
                </Col>
            </Row>
            <Row className='align-items-left'>
                <Col>
                    <p>{t('instructions.description')}</p>
                </Col>
            </Row>
            <h2>{t('instructions.goal.title')}</h2>
            <Row>
                <Col >
                    <p>{t('instructions.goal.description')}</p>
                </Col>
            </Row>            
        </Container>
    );
}

export default Instructions;
