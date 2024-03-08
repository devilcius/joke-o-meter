import React from 'react';
import { Outlet } from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import Header from './Header';
import Footer from './Footer';
import '../i18n';

const Root = () => {


    return (
        <main id="jokeometer">
            <Container>
                <Header />
                <Outlet />
                <Footer />
            </Container>
        </main>
    );
};

export default Root;