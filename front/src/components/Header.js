import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGlobe } from '@fortawesome/free-solid-svg-icons';
import { useTranslation } from 'react-i18next';

import { t } from 'i18next';
import '../css/Header.css';

const Header = () => {

  const [active, setActive] = useState('home');
  const { i18n } = useTranslation();


  return (
    <Navbar >
        <Navbar.Brand as={Link} to="/" >
          <img src='/logo192-black.png'
            width="24" height="24"
            alt="Logo" />
          <span>Joke-O-Meter</span>
        </Navbar.Brand>
        <Navbar/>
          <Nav
            className="ml-auto"
            activeKey={active}
            onSelect={(selectedKey) => setActive(selectedKey)}
          >
            <Nav.Link as={Link} to="/swipe" eventKey="swipe" role="link" >
              {t('welcome.start')}
            </Nav.Link>           
            <Nav.Link as={Link} to="/instructions" eventKey="instructions" role="link" >
              {t('welcome.instructions')}
            </Nav.Link>
            <Nav.Link as={Link} to="/ranking" eventKey="ranking" role="link" >
              {t('ranking.title')}
            </Nav.Link>
            <NavDropdown title={<FontAwesomeIcon icon={faGlobe} align="left" />} id="basic-nav-dropdown" >
              <NavDropdown.Item onClick={() => i18n.changeLanguage('en')}>English</NavDropdown.Item>
              <NavDropdown.Item onClick={() => i18n.changeLanguage('es')}>Español</NavDropdown.Item>
            </NavDropdown>             
          </Nav>
    </Navbar>
  );
};

export default Header;
