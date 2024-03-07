import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Container, Navbar, Nav } from 'react-bootstrap';
import { t } from 'i18next';

const Header = () => {

  const [active, setActive] = useState('home');

  return (
    <Navbar >
      <Container>
        <Navbar.Brand as={Link} to="/" >Joke-O-Meter</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav
            className="ml-auto"
            activeKey={active}
            onSelect={(selectedKey) => setActive(selectedKey)}
          >
            <Nav.Link as={Link} to="/swipe" eventKey="play" role="link" >
              {t('welcome.play')}
            </Nav.Link>
            <Nav.Link as={Link} to="/instructions" eventKey="instructions" role="link" >
              {t('welcome.instructions')}
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Header;
