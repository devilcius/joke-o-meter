import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom'
import { BrowserRouter as Router } from 'react-router-dom';
import { act } from 'react-dom/test-utils';
import Header from '../Header';
import i18n from '../../i18n';
import { I18nextProvider } from 'react-i18next'

describe('Header Component', () => {
  test('renders the header with correct links', async () => {
    const component = render(
      <I18nextProvider i18n={i18n}> // actually give translation to your component
        <Router>
          <Header />
        </Router>
      </I18nextProvider>
    );
    // Check if the "Play" link is rendered correctly
    expect(component.getByText(i18n.getDataByLanguage('en').translation['welcome.play'])).toBeDefined();
    // Check if the "Instructions" link is rendered correctly
    expect(component.getByText(i18n.getDataByLanguage('en').translation['welcome.instructions'])).toBeDefined();
    // Check if the brand name is rendered correctly
    const brandName = screen.getByText('Joke-O-Meter');
    expect(brandName).toBeInTheDocument();
    // Check if the "Instructions" link becomes active when clicked
    const instructionsLink = component.getByText(i18n.getDataByLanguage('en').translation['welcome.instructions']);
    await act(async () => {
      instructionsLink.click();
    });

    await waitFor(() => {
      expect(instructionsLink).toHaveClass('active');
    });
  });
});