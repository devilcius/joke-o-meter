import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Container, Navbar, Nav } from 'react-bootstrap';
import { t } from 'i18next';
import '../css/Header.css';

const Header = () => {

  const [active, setActive] = useState('home');

  return (
    <Navbar >
      <Container>
        <Navbar.Brand as={Link} to="/" >
          <img src='/logo192-black.png'
            width="24" height="24"
            alt="Logo" />
          <span>Joke-O-Meter</span>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
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
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;
