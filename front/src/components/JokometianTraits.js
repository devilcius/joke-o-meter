import React from "react";
import { useTranslation } from 'react-i18next';
import Table from 'react-bootstrap/Table';

const JokometianTraits = ({traits}) => {
    const { t } = useTranslation();
    const TRAITS_MAPPER = {
        'RACE': {
            'name': t('jokometian.trait_incandescent'),
            'emoji': '🔥'
        },
        'RELIGION': {
            'name': t('jokometian.trait_spiritual'),
            'emoji': '🕍'
        },
        'ETHNICITY': {
            'name': t('jokometian.trait_diversity'),
            'emoji': '🌍'
        },
        'GENDER': {
            'name': t('jokometian.trait_wise'),
            'emoji': '👴'
        },
        'SEXUAL_ORIENTATION': {
            'name': t('jokometian.trait_radiant'),
            'emoji': '🌈'
        },
        'DISABILITY': {
            'name': t('jokometian.trait_resilient'),
            'emoji': '🦿'
        },
        'GENERIC_VIOLENCE': {
            'name': t('jokometian.trait_fierce'),
            'emoji': '🗡️'
        },
        'NO_OFFENSE_FOUND': {
            'name': t('jokometian.trait_pure_soul'),
            'emoji': '😇'
        },        
    };    

    const traitsContent = traits.map((trait, index) => {
        return (
            <tr key={index}>
                <td>{TRAITS_MAPPER[trait.name].emoji}{' '}{TRAITS_MAPPER[trait.name].name}</td>
                <td>{trait.degree}</td>
            </tr>
        );
    }
    );

    return (
        <Table striped bordered hover>
            <tbody>
                {traitsContent}
            </tbody>
        </Table>
    );
}

export default JokometianTraits;