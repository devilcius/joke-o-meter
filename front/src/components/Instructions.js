import React from 'react';
import { Container, Row, Col, ListGroup } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSmileBeam, faFrownOpen, faHandPointer } from '@fortawesome/free-solid-svg-icons';
import { useTranslation } from 'react-i18next';
import '../css/Instructions.css';

const Instructions = () => {
    const { t } = useTranslation();
    return (
        <Container className="my-4 jokeometer-instuctions">
            <h1>{t('instructions.title')}</h1>
            <Row className="text-center align-items-center my-3">
                <Col >
                    <FontAwesomeIcon icon={faFrownOpen} size="3x" color="red" />
                </Col>
                <Col>
                    <FontAwesomeIcon icon={faSmileBeam} size="3x" color="green" />
                </Col>
            </Row>
            <Row lg="10" className='text-center align-items-center my-3'>
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
            <h2>{t('instructions.motivation.title')}</h2>
            <Row>
                <Col>
                    <p>{t('instructions.motivation.description')}</p>
                </Col>
            </Row>
            <h2>{t('instructions.characters.title')}</h2>
            <Row>
                <Col>
                    <p>{t('instructions.characters.introduction')}</p>
                </Col>
            </Row>
            <Row>
                <Col>
                    <ListGroup>
                        <ListGroup.Item>{t('jokometian.trait_wise') + " ➡️ "} <strong><span className="text-info">{t('instructions.characters.trait_wise')}</span></strong></ListGroup.Item>
                        <ListGroup.Item>{t('jokometian.trait_spiritual') + " ➡️ "} <strong><span className="text-info">{t('instructions.characters.trait_spiritual')}</span></strong></ListGroup.Item>
                        <ListGroup.Item>{t('jokometian.trait_resilient') + " ➡️ "} <strong><span className="text-info">{t('instructions.characters.trait_resilient')}</span></strong></ListGroup.Item>
                        <ListGroup.Item>{t('jokometian.trait_radiant') + " ➡️ "} <strong><span className="text-info">{t('instructions.characters.trait_radiant')}</span></strong></ListGroup.Item>
                        <ListGroup.Item>{t('jokometian.trait_incandescent') + " ➡️ "} <strong><span className="text-info">{ t('instructions.characters.trait_incandescent')}</span></strong></ListGroup.Item>
                        <ListGroup.Item>{t('jokometian.trait_fierce') + " ➡️ "} <strong><span className="text-info">{ t('instructions.characters.trait_fierce')}</span></strong></ListGroup.Item>
                        <ListGroup.Item>{t('jokometian.trait_diversity') + " ➡️ "} <strong><span className="text-info">{ t('instructions.characters.trait_diversity')}</span></strong></ListGroup.Item>
                        <hr/>
                        <ListGroup.Item>{t('jokometian.trait_pure_soul') + " ➡️ "} <strong><span className="text-info">{ t('instructions.characters.trait_pure_soul')}</span></strong></ListGroup.Item>
                        <ListGroup.Item>{t('jokometian.trait_grumpy') + " ➡️ "} <strong><span className="text-info">{ t('instructions.characters.trait_grumpy')}</span></strong></ListGroup.Item>
                        <ListGroup.Item>{t('jokometian.trait_giggly') + " ➡️ "} <strong><span className="text-info">{ t('instructions.characters.trait_giggly')}</span></strong></ListGroup.Item>
                        <ListGroup.Item>{t('jokometian.trait_diabolical') + " ➡️ "} <strong><span className="text-info">{ t('instructions.characters.trait_diabolical')}</span></strong></ListGroup.Item>
                    </ListGroup>
                </Col>
            </Row>
        </Container>
    );
}

export default Instructions;
