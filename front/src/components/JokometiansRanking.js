import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Container, Row, Table } from 'react-bootstrap';
import { fetchJokometiansRanking } from '../api/jokometians_ranking';
import { getJokometianTraitMapper } from '../utils/index';

const JokometiansRanking = () => {
    const { t } = useTranslation();
    const TRAITS_MAPPER = getJokometianTraitMapper(t);
    const [rankings, setRankings] = useState([]);

    useEffect(() => {
        const loadRankings = async () => {
            const response = await fetchJokometiansRanking();
            if (response.status === 200) {
                setRankings(response.data);
            } else {
                // Handle errors or invalid responses
                console.error('Failed to fetch rankings:', response);
            }
        };

        loadRankings();
    }, []);

    return (
        <Container>
            <Row>
                <h1>{t('ranking.title')}</h1>
                <p className="mb-4">{t('ranking.description')}</p>
                <Table striped>
                    <tbody>
                        {rankings.map((ranking, index) => (
                            <tr key={index}>
                                <td><h2>{index + 1}</h2></td>
                                <td><img src={ranking.image_url} alt={ranking.name} style={{ width: '50px', height: '50px' }} /></td>
                                <td>{TRAITS_MAPPER[ranking.name].trait}</td>
                                <td>{ranking.score}</td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            </Row>
        </Container>
    );
};

export default JokometiansRanking;
