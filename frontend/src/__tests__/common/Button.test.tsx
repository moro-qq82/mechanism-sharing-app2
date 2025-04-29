import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../../components/common/Button';

describe('Button Component', () => {
  test('renders button with default props', () => {
    render(<Button>テストボタン</Button>);
    const button = screen.getByRole('button', { name: /テストボタン/i });
    expect(button).toBeInTheDocument();
    expect(button).toHaveClass('bg-blue-600'); // primary variant
  });

  test('renders button with different variants', () => {
    const { rerender } = render(<Button variant="secondary">セカンダリ</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-gray-600');

    rerender(<Button variant="danger">危険</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-red-600');

    rerender(<Button variant="success">成功</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-green-600');

    rerender(<Button variant="outline">アウトライン</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-transparent');
  });

  test('renders button with different sizes', () => {
    const { rerender } = render(<Button size="sm">小</Button>);
    expect(screen.getByRole('button')).toHaveClass('py-1 px-3 text-sm');

    rerender(<Button size="md">中</Button>);
    expect(screen.getByRole('button')).toHaveClass('py-2 px-4 text-base');

    rerender(<Button size="lg">大</Button>);
    expect(screen.getByRole('button')).toHaveClass('py-3 px-6 text-lg');
  });

  test('renders full width button', () => {
    render(<Button fullWidth>全幅</Button>);
    expect(screen.getByRole('button')).toHaveClass('w-full');
  });

  test('renders loading state', () => {
    render(<Button isLoading>ロード中</Button>);
    expect(screen.getByText('読み込み中...')).toBeInTheDocument();
    expect(screen.queryByText('ロード中')).not.toBeInTheDocument();
  });

  test('button is disabled when disabled prop is true', () => {
    render(<Button disabled>無効</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  test('button is disabled when loading', () => {
    render(<Button isLoading>ロード中</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  test('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>クリック</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('does not call onClick when disabled', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick} disabled>クリック</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).not.toHaveBeenCalled();
  });

  test('does not call onClick when loading', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick} isLoading>クリック</Button>);
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).not.toHaveBeenCalled();
  });
});
