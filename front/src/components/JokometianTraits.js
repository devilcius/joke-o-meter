import React from "react";
import { useTranslation } from 'react-i18next';
import Table from 'react-bootstrap/Table';
import { getJokometianTraitMapper } from '../utils/index';

const JokometianTraits = ({ traits }) => {
    const { t } = useTranslation();
    const TRAITS_MAPPER = getJokometianTraitMapper(t);

    const traitsContent = traits.map((trait, index) => {
        return (
            <tr key={index}>
                <td>{TRAITS_MAPPER[trait.name].emoji}{' '}{TRAITS_MAPPER[trait.name].trait}</td>
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