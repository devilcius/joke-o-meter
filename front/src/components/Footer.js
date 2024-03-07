import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  return (
    <footer className="fixed-bottom bg-footer">
      <Container>
        <Row>
          <Col md={6}>
            <p>{currentYear} Joke-O-Meter</p>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;
