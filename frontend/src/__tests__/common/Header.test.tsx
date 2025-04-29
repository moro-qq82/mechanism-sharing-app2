import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Header } from '../../components/common/Header';
import Button from '../../components/common/Button';

// ラッパーコンポーネントを作成してBrowserRouterを提供
const renderWithRouter = (ui: React.ReactElement) => {
  return render(<BrowserRouter>{ui}</BrowserRouter>);
};

describe('Header Component', () => {
  test('renders title correctly', () => {
    renderWithRouter(<Header title="テストタイトル" />);
    expect(screen.getByTestId('header-title')).toHaveTextContent('テストタイトル');
  });

  test('renders subtitle when provided', () => {
    renderWithRouter(<Header title="テストタイトル" subtitle="テストサブタイトル" />);
    expect(screen.getByTestId('header-subtitle')).toHaveTextContent('テストサブタイトル');
  });

  test('does not render subtitle when not provided', () => {
    renderWithRouter(<Header title="テストタイトル" />);
    expect(screen.queryByTestId('header-subtitle')).not.toBeInTheDocument();
  });

  test('renders back link when backLink is provided', () => {
    renderWithRouter(<Header title="テストタイトル" backLink="/back" />);
    const backLink = screen.getByTestId('header-back-link');
    expect(backLink).toBeInTheDocument();
    expect(backLink).toHaveAttribute('href', '/back');
    expect(backLink).toHaveTextContent('戻る');
  });

  test('renders custom back text when provided', () => {
    renderWithRouter(<Header title="テストタイトル" backLink="/back" backText="前のページ" />);
    expect(screen.getByTestId('header-back-link')).toHaveTextContent('前のページ');
  });

  test('does not render back link when backLink is not provided', () => {
    renderWithRouter(<Header title="テストタイトル" />);
    expect(screen.queryByTestId('header-back-link')).not.toBeInTheDocument();
  });

  test('renders action button when provided', () => {
    renderWithRouter(
      <Header 
        title="テストタイトル" 
        actionButton={<Button>アクション</Button>} 
      />
    );
    const actionContainer = screen.getByTestId('header-action');
    expect(actionContainer).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'アクション' })).toBeInTheDocument();
  });

  test('does not render action button when not provided', () => {
    renderWithRouter(<Header title="テストタイトル" />);
    expect(screen.queryByTestId('header-action')).not.toBeInTheDocument();
  });

  test('applies custom className', () => {
    renderWithRouter(<Header title="テストタイトル" className="custom-header" />);
    const header = screen.getByRole('banner');
    expect(header).toHaveClass('custom-header');
  });
});
