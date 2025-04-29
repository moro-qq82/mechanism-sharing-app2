import React from 'react';
import { render, screen } from '@testing-library/react';
import { Loading } from '../../components/common/Loading';

describe('Loading Component', () => {
  test('renders loading spinner', () => {
    render(<Loading />);
    const spinner = screen.getByTestId('loading-spinner');
    expect(spinner).toBeInTheDocument();
  });

  test('renders with small size', () => {
    render(<Loading size="sm" />);
    const spinner = screen.getByTestId('loading-spinner');
    expect(spinner).toHaveClass('w-5 h-5');
  });

  test('renders with medium size', () => {
    render(<Loading size="md" />);
    const spinner = screen.getByTestId('loading-spinner');
    expect(spinner).toHaveClass('w-8 h-8');
  });

  test('renders with large size', () => {
    render(<Loading size="lg" />);
    const spinner = screen.getByTestId('loading-spinner');
    expect(spinner).toHaveClass('w-12 h-12');
  });

  test('renders with default medium size when not specified', () => {
    render(<Loading />);
    const spinner = screen.getByTestId('loading-spinner');
    expect(spinner).toHaveClass('w-8 h-8');
  });

  test('renders with custom color', () => {
    render(<Loading color="text-red-500" />);
    const spinner = screen.getByTestId('loading-spinner');
    expect(spinner).toHaveClass('text-red-500');
  });

  test('renders with default blue color when not specified', () => {
    render(<Loading />);
    const spinner = screen.getByTestId('loading-spinner');
    expect(spinner).toHaveClass('text-blue-600');
  });

  test('renders with loading text', () => {
    render(<Loading text="読み込み中..." />);
    expect(screen.getByText('読み込み中...')).toBeInTheDocument();
  });

  test('does not render text when not provided', () => {
    render(<Loading />);
    expect(screen.queryByText(/読み込み中/)).not.toBeInTheDocument();
  });

  test('renders with fullScreen mode', () => {
    render(<Loading fullScreen />);
    expect(screen.getByTestId('loading-fullscreen')).toBeInTheDocument();
    expect(screen.getByTestId('loading-fullscreen')).toHaveClass('fixed inset-0 bg-white bg-opacity-75 z-50');
  });

  test('renders without fullScreen mode by default', () => {
    render(<Loading />);
    expect(screen.queryByTestId('loading-fullscreen')).not.toBeInTheDocument();
  });

  test('applies custom className', () => {
    render(<Loading className="custom-loading" />);
    expect(screen.getByTestId('loading-container')).toHaveClass('custom-loading');
  });
});
