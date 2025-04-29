import React from 'react';
import { Link } from 'react-router-dom';

export interface FooterLink {
  text: string;
  href: string;
  external?: boolean;
}

export interface FooterProps {
  copyright?: string;
  links?: FooterLink[];
  className?: string;
}

export const Footer: React.FC<FooterProps> = ({
  copyright = `© ${new Date().getFullYear()} メカニズム共有プラットフォーム`,
  links = [],
  className = '',
}) => {
  return (
    <footer 
      className={`py-6 bg-gray-100 mt-auto ${className}`}
      data-testid="footer"
    >
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-gray-600 text-sm" data-testid="footer-copyright">
              {copyright}
            </p>
          </div>
          {links.length > 0 && (
            <nav className="flex flex-wrap justify-center gap-x-6 gap-y-2">
              {links.map((link, index) => (
                link.external ? (
                  <a
                    key={index}
                    href={link.href}
                    className="text-blue-600 hover:text-blue-800 text-sm"
                    target="_blank"
                    rel="noopener noreferrer"
                    data-testid={`footer-external-link-${index}`}
                  >
                    {link.text}
                  </a>
                ) : (
                  <Link
                    key={index}
                    to={link.href}
                    className="text-blue-600 hover:text-blue-800 text-sm"
                    data-testid={`footer-link-${index}`}
                  >
                    {link.text}
                  </Link>
                )
              ))}
            </nav>
          )}
        </div>
      </div>
    </footer>
  );
};

export default Footer;
