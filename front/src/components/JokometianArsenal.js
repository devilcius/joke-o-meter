import React from "react";
import Table from 'react-bootstrap/Table';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBomb } from '@fortawesome/free-solid-svg-icons';
import { useTranslation } from 'react-i18next';

const JokometianArsenal = ({ jokometian }) => {
    const { t } = useTranslation();
    // Function to determine the color based on the joke's offense degree
    const getOffenseColor = (degree) => {
        // Map degree to hue: 0 (degree) -> 120 (green), 10 (degree) -> 0 (red)
        const hue = 120 - (degree * 12); // Scale degree from 0-10 to 120-0 hue value
        return `hsl(${hue}, 100%, 50%)`; // Use the HSL color model
    };
    const sortedJokes = jokometian.jokes.sort((a, b) => b.trait.degree - a.trait.degree);
    if(sortedJokes.length === 0) return (<p>{t('jokometian.empty_jokes_notice')}</p>);

    const jokesContent = sortedJokes.map((joke, index) => {
        return (
            <tr key={index}>
                <td>
                    <FontAwesomeIcon icon={faBomb} color={getOffenseColor(joke.trait.degree)} />
                    <span style={{ marginLeft: "10px" }}>{joke.content}</span>
                </td>
            </tr>
        );
    });

    return (
        <Table striped bordered hover>
            <tbody>
                {jokesContent}
            </tbody>
        </Table>
    );
};

export default JokometianArsenal;
