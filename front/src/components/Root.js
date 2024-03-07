import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import '../i18n';

const Root = () => {


    return (
        <main id="jokeometer">
            <Header  />
            <Outlet />
            <Footer />
        </main>
    );
};

export default Root;