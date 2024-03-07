import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import '../css/JokometianView.css';
import { fetchJokometian } from '../api/jokometians';
import { useTranslation } from 'react-i18next';
import Card from 'react-bootstrap/Card';
import JokometianTraits from './JokometianTraits';

const JokometianView = () => {
    const { t } = useTranslation();
    const { id } = useParams();
    const [jokometian, setJokometian] = React.useState({});

    useEffect(() => {
        const fetchJokometianData = async () => {
            const response = await fetchJokometian(id);
            if (response.status === 200) {
                setJokometian(response.data);
            }
        };
        fetchJokometianData();
    }, [id]);

    if (Object.keys(jokometian).length === 0) {
        return <div>{t('jokometian.loading')}</div>;
    }

    return (
        <div className="d-flex align-items-center justify-content-center jokometian-view-container">
            <Card style={{ width: '25rem' }} className='shadow-lg p-3 mb-5 bg-white rounded'>
                <Card.Header>{t('jokometian.title')}</Card.Header>
                <Card.Img variant="top" src={jokometian.image_url} />
                <Card.Body>
                    <Card.Title>{jokometian.name}</Card.Title>
                    <Card.Text>
                        {jokometian.description}
                        <hr/>
                        <JokometianTraits traits={jokometian.traits} />
                    </Card.Text>
                </Card.Body>
            </Card>
        </div>
    );
}


export default JokometianView;