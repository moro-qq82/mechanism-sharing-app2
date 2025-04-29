import React from 'react';
import { Link } from 'react-router-dom';

export interface HeaderProps {
  title: string;
  subtitle?: string;
  backLink?: string;
  backText?: string;
  actionButton?: React.ReactNode;
  className?: string;
}

export const Header: React.FC<HeaderProps> = ({
  title,
  subtitle,
  backLink,
  backText = '戻る',
  actionButton,
  className = '',
}) => {
  return (
    <header className={`mb-6 ${className}`}>
      <div className="flex justify-between items-center mb-2">
        <div className="flex items-center">
          {backLink && (
            <Link
              to={backLink}
              className="mr-4 text-blue-600 hover:text-blue-800 flex items-center"
              data-testid="header-back-link"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5 mr-1"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
                  clipRule="evenodd"
                />
              </svg>
              {backText}
            </Link>
          )}
          <h1 
            className="text-2xl font-bold text-gray-900"
            data-testid="header-title"
          >
            {title}
          </h1>
        </div>
        {actionButton && (
          <div data-testid="header-action">
            {actionButton}
          </div>
        )}
      </div>
      {subtitle && (
        <p 
          className="text-gray-600"
          data-testid="header-subtitle"
        >
          {subtitle}
        </p>
      )}
    </header>
  );
};

export default Header;
