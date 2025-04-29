import React, { InputHTMLAttributes, forwardRef, useState, useRef } from 'react';
import Button from './Button';

export interface FileUploadProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string;
  error?: string;
  helperText?: string;
  fullWidth?: boolean;
  buttonText?: string;
  acceptedFileTypes?: string;
  showSelectedFileName?: boolean;
}

export const FileUpload = forwardRef<HTMLInputElement, FileUploadProps>(
  ({
    label,
    error,
    helperText,
    fullWidth = false,
    buttonText = 'ファイルを選択',
    acceptedFileTypes,
    showSelectedFileName = true,
    className = '',
    onChange,
    ...props
  }, ref) => {
    const [fileName, setFileName] = useState<string>('');
    const inputRef = useRef<HTMLInputElement | null>(null);
    
    // refの転送
    const setRefs = (element: HTMLInputElement) => {
      inputRef.current = element;
      if (typeof ref === 'function') {
        ref(element);
      } else if (ref) {
        ref.current = element;
      }
    };

    const handleButtonClick = () => {
      if (inputRef.current) {
        inputRef.current.click();
      }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files;
      if (files && files.length > 0) {
        setFileName(files[0].name);
      } else {
        setFileName('');
      }
      
      if (onChange) {
        onChange(e);
      }
    };

    return (
      <div className={`mb-4 ${fullWidth ? 'w-full' : ''}`}>
        {label && (
          <label
            htmlFor={props.id}
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            {label}
          </label>
        )}
        <div className="flex flex-col sm:flex-row gap-2">
          <input
            ref={setRefs}
            type="file"
            accept={acceptedFileTypes}
            className="hidden"
            onChange={handleFileChange}
            aria-invalid={error ? 'true' : 'false'}
            {...props}
          />
          <Button
            type="button"
            onClick={handleButtonClick}
            variant="outline"
            className={className}
          >
            {buttonText}
          </Button>
          {showSelectedFileName && (
            <div className="flex items-center text-sm text-gray-600 overflow-hidden">
              {fileName ? (
                <span className="truncate">{fileName}</span>
              ) : (
                <span className="text-gray-400">ファイルが選択されていません</span>
              )}
            </div>
          )}
        </div>
        {error && (
          <p className="mt-1 text-sm text-red-600" id={`${props.id}-error`}>
            {error}
          </p>
        )}
        {helperText && !error && (
          <p className="mt-1 text-sm text-gray-500" id={`${props.id}-helper-text`}>
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

FileUpload.displayName = 'FileUpload';

export default FileUpload;
