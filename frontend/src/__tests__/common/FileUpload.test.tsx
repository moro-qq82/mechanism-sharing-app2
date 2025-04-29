import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { FileUpload } from '../../components/common/FileUpload';

// モックファイル作成のヘルパー関数
const createFile = (name: string, size: number, type: string): File => {
  const file = new File([], name, { type });
  Object.defineProperty(file, 'size', {
    get() {
      return size;
    }
  });
  return file;
};

describe('FileUpload Component', () => {
  test('renders file upload button', () => {
    render(<FileUpload />);
    const button = screen.getByRole('button', { name: /ファイルを選択/i });
    expect(button).toBeInTheDocument();
  });

  test('renders with custom button text', () => {
    render(<FileUpload buttonText="画像をアップロード" />);
    const button = screen.getByRole('button', { name: /画像をアップロード/i });
    expect(button).toBeInTheDocument();
  });

  test('renders with label', () => {
    render(<FileUpload id="test-upload" label="ファイルアップロード" />);
    const label = screen.getByText('ファイルアップロード');
    expect(label).toBeInTheDocument();
    expect(label.tagName).toBe('LABEL');
    expect(label).toHaveAttribute('for', 'test-upload');
  });

  test('renders with error message', () => {
    render(<FileUpload id="test-upload" error="エラーメッセージ" />);
    const errorMessage = screen.getByText('エラーメッセージ');
    expect(errorMessage).toBeInTheDocument();
    expect(errorMessage).toHaveAttribute('id', 'test-upload-error');
  });

  test('renders with helper text', () => {
    render(<FileUpload id="test-upload" helperText="ヘルパーテキスト" />);
    const helperText = screen.getByText('ヘルパーテキスト');
    expect(helperText).toBeInTheDocument();
    expect(helperText).toHaveAttribute('id', 'test-upload-helper-text');
  });

  test('does not render helper text when error is present', () => {
    render(
      <FileUpload 
        id="test-upload" 
        error="エラーメッセージ" 
        helperText="ヘルパーテキスト" 
      />
    );
    expect(screen.getByText('エラーメッセージ')).toBeInTheDocument();
    expect(screen.queryByText('ヘルパーテキスト')).not.toBeInTheDocument();
  });

  test('shows default message when no file is selected', () => {
    render(<FileUpload />);
    expect(screen.getByText('ファイルが選択されていません')).toBeInTheDocument();
  });

  test('updates file name when file is selected', () => {
    render(<FileUpload data-testid="test-upload" />);
    
    const file = createFile('test.jpg', 1024, 'image/jpeg');
    const input = screen.getByTestId('test-upload');
    
    Object.defineProperty(input, 'files', {
      value: [file]
    });
    
    fireEvent.change(input);
    
    expect(screen.getByText('test.jpg')).toBeInTheDocument();
  });

  test('hides file name when showSelectedFileName is false', () => {
    render(<FileUpload showSelectedFileName={false} />);
    expect(screen.queryByText('ファイルが選択されていません')).not.toBeInTheDocument();
  });

  test('forwards ref to input element', () => {
    const ref = React.createRef<HTMLInputElement>();
    render(<FileUpload ref={ref} data-testid="test-upload" />);
    expect(ref.current).toBe(screen.getByTestId('test-upload'));
  });

  test('calls onChange handler when file is selected', () => {
    const handleChange = jest.fn();
    render(<FileUpload onChange={handleChange} data-testid="test-upload" />);
    
    const file = createFile('test.jpg', 1024, 'image/jpeg');
    const input = screen.getByTestId('test-upload');
    
    Object.defineProperty(input, 'files', {
      value: [file]
    });
    
    fireEvent.change(input);
    
    expect(handleChange).toHaveBeenCalledTimes(1);
  });

  test('sets accepted file types', () => {
    render(<FileUpload acceptedFileTypes=".jpg,.png" data-testid="test-upload" />);
    const input = screen.getByTestId('test-upload');
    expect(input).toHaveAttribute('accept', '.jpg,.png');
  });
});
