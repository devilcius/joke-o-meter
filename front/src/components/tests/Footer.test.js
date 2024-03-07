import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom'
import Footer from '../Footer';

describe('Footer component', () => {
  it('renders the current year', () => {
    render(<Footer />);
    const currentYear = new Date().getFullYear();
    expect(screen.getByText((content, element) => {
      return content.includes('Joke-O-Meter') && content.includes(currentYear);
    })).toBeInTheDocument();
  });
});