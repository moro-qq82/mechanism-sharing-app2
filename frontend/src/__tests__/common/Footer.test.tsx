import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Footer } from '../../components/common/Footer';

// ラッパーコンポーネントを作成してBrowserRouterを提供
const renderWithRouter = (ui: React.ReactElement) => {
  return render(<BrowserRouter>{ui}</BrowserRouter>);
};

describe('Footer Component', () => {
  test('renders footer with default copyright', () => {
    renderWithRouter(<Footer />);
    const footer = screen.getByTestId('footer');
    expect(footer).toBeInTheDocument();
    
    const currentYear = new Date().getFullYear();
    expect(screen.getByTestId('footer-copyright')).toHaveTextContent(
      `© ${currentYear} メカニズム共有プラットフォーム`
    );
  });

  test('renders footer with custom copyright', () => {
    renderWithRouter(<Footer copyright="© 2025 テスト" />);
    expect(screen.getByTestId('footer-copyright')).toHaveTextContent('© 2025 テスト');
  });

  test('renders internal links correctly', () => {
    const links = [
      { text: 'ホーム', href: '/' },
      { text: '利用規約', href: '/terms' },
    ];
    
    renderWithRouter(<Footer links={links} />);
    
    const homeLink = screen.getByTestId('footer-link-0');
    expect(homeLink).toHaveTextContent('ホーム');
    expect(homeLink).toHaveAttribute('href', '/');
    
    const termsLink = screen.getByTestId('footer-link-1');
    expect(termsLink).toHaveTextContent('利用規約');
    expect(termsLink).toHaveAttribute('href', '/terms');
  });

  test('renders external links correctly', () => {
    const links = [
      { text: 'GitHub', href: 'https://github.com', external: true },
    ];
    
    renderWithRouter(<Footer links={links} />);
    
    const githubLink = screen.getByTestId('footer-external-link-0');
    expect(githubLink).toHaveTextContent('GitHub');
    expect(githubLink).toHaveAttribute('href', 'https://github.com');
    expect(githubLink).toHaveAttribute('target', '_blank');
    expect(githubLink).toHaveAttribute('rel', 'noopener noreferrer');
  });

  test('renders both internal and external links', () => {
    const links = [
      { text: 'ホーム', href: '/' },
      { text: 'GitHub', href: 'https://github.com', external: true },
    ];
    
    renderWithRouter(<Footer links={links} />);
    
    expect(screen.getByTestId('footer-link-0')).toBeInTheDocument();
    expect(screen.getByTestId('footer-external-link-1')).toBeInTheDocument();
  });

  test('does not render nav when no links are provided', () => {
    renderWithRouter(<Footer />);
    expect(screen.queryByRole('navigation')).not.toBeInTheDocument();
  });

  test('applies custom className', () => {
    renderWithRouter(<Footer className="custom-footer" />);
    expect(screen.getByTestId('footer')).toHaveClass('custom-footer');
  });
});
