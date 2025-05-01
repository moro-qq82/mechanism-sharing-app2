import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders login page', () => {
  render(<App />);
  const loginHeading = screen.getByRole('heading', { name: /ログイン/i });
  expect(loginHeading).toBeInTheDocument();
});
