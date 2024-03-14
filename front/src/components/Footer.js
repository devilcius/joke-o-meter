import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGithub } from '@fortawesome/free-brands-svg-icons';
import { faBlog } from '@fortawesome/free-solid-svg-icons';

import { t } from 'i18next';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  return (
    <footer className="fixed-bottom bg-footer footer">
      <Container>
        <Row className='align-items-center'>
          <Col  className="d-flex justify-content-left">
            <p>{currentYear} Joke-O-Meter</p>
          </Col>
          <Col  className="d-flex justify-content-end gap-2 mr-4">
            <a
              href="https://github.com/devilcius/joke-o-meter"
              target="_blank"
              rel="noopener noreferrer"
              title={t('footer.github_title')}
            >
              <FontAwesomeIcon icon={faGithub} className='text-black' />
            </a>          
            <a
              href="https://blog.marcospena.es/el-chistometro"
              target="_blank"
              rel="noopener noreferrer"
              title={t('footer.blog_title')}
            >
              <FontAwesomeIcon icon={faBlog} className='text-black' />
            </a>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;
