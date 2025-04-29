import React from 'react';
import { render, screen } from '@testing-library/react';
import { TextArea } from '../../components/common/TextArea';

describe('TextArea Component', () => {
  test('renders textarea element', () => {
    render(<TextArea data-testid="test-textarea" />);
    const textarea = screen.getByTestId('test-textarea');
    expect(textarea).toBeInTheDocument();
    expect(textarea.tagName).toBe('TEXTAREA');
  });

  test('renders with label', () => {
    render(<TextArea id="test-textarea" label="テストラベル" />);
    const label = screen.getByText('テストラベル');
    expect(label).toBeInTheDocument();
    expect(label.tagName).toBe('LABEL');
    expect(label).toHaveAttribute('for', 'test-textarea');
  });

  test('renders with placeholder', () => {
    render(<TextArea placeholder="テストプレースホルダー" />);
    const textarea = screen.getByPlaceholderText('テストプレースホルダー');
    expect(textarea).toBeInTheDocument();
  });

  test('renders with error message', () => {
    render(<TextArea id="test-textarea" error="エラーメッセージ" />);
    const errorMessage = screen.getByText('エラーメッセージ');
    expect(errorMessage).toBeInTheDocument();
    expect(errorMessage).toHaveAttribute('id', 'test-textarea-error');
    
    const textarea = screen.getByRole('textbox');
    expect(textarea).toHaveAttribute('aria-invalid', 'true');
    expect(textarea).toHaveClass('border-red-500');
  });

  test('renders with helper text', () => {
    render(<TextArea id="test-textarea" helperText="ヘルパーテキスト" />);
    const helperText = screen.getByText('ヘルパーテキスト');
    expect(helperText).toBeInTheDocument();
    expect(helperText).toHaveAttribute('id', 'test-textarea-helper-text');
  });

  test('does not render helper text when error is present', () => {
    render(
      <TextArea 
        id="test-textarea" 
        error="エラーメッセージ" 
        helperText="ヘルパーテキスト" 
      />
    );
    expect(screen.getByText('エラーメッセージ')).toBeInTheDocument();
    expect(screen.queryByText('ヘルパーテキスト')).not.toBeInTheDocument();
  });

  test('renders full width textarea', () => {
    render(<TextArea fullWidth data-testid="test-textarea" />);
    expect(screen.getByTestId('test-textarea')).toHaveClass('w-full');
  });

  test('forwards ref to textarea element', () => {
    const ref = React.createRef<HTMLTextAreaElement>();
    render(<TextArea ref={ref} data-testid="test-textarea" />);
    expect(ref.current).toBe(screen.getByTestId('test-textarea'));
  });

  test('passes additional props to textarea element', () => {
    render(
      <TextArea 
        name="description" 
        required 
        disabled 
        data-testid="test-textarea" 
      />
    );
    const textarea = screen.getByTestId('test-textarea');
    expect(textarea).toHaveAttribute('name', 'description');
    expect(textarea).toHaveAttribute('required');
    expect(textarea).toBeDisabled();
  });

  test('renders with custom number of rows', () => {
    render(<TextArea rows={8} data-testid="test-textarea" />);
    const textarea = screen.getByTestId('test-textarea');
    expect(textarea).toHaveAttribute('rows', '8');
  });

  test('renders with default number of rows when not specified', () => {
    render(<TextArea data-testid="test-textarea" />);
    const textarea = screen.getByTestId('test-textarea');
    expect(textarea).toHaveAttribute('rows', '4');
  });
});
