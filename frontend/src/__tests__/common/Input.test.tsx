import React from 'react';
import { render, screen } from '@testing-library/react';
import { Input } from '../../components/common/Input';

describe('Input Component', () => {
  test('renders input element', () => {
    render(<Input data-testid="test-input" />);
    const input = screen.getByTestId('test-input');
    expect(input).toBeInTheDocument();
    expect(input.tagName).toBe('INPUT');
  });

  test('renders with label', () => {
    render(<Input id="test-input" label="テストラベル" />);
    const label = screen.getByText('テストラベル');
    expect(label).toBeInTheDocument();
    expect(label.tagName).toBe('LABEL');
    expect(label).toHaveAttribute('for', 'test-input');
  });

  test('renders with placeholder', () => {
    render(<Input placeholder="テストプレースホルダー" />);
    const input = screen.getByPlaceholderText('テストプレースホルダー');
    expect(input).toBeInTheDocument();
  });

  test('renders with error message', () => {
    render(<Input id="test-input" error="エラーメッセージ" />);
    const errorMessage = screen.getByText('エラーメッセージ');
    expect(errorMessage).toBeInTheDocument();
    expect(errorMessage).toHaveAttribute('id', 'test-input-error');
    
    const input = screen.getByRole('textbox');
    expect(input).toHaveAttribute('aria-invalid', 'true');
    expect(input).toHaveClass('border-red-500');
  });

  test('renders with helper text', () => {
    render(<Input id="test-input" helperText="ヘルパーテキスト" />);
    const helperText = screen.getByText('ヘルパーテキスト');
    expect(helperText).toBeInTheDocument();
    expect(helperText).toHaveAttribute('id', 'test-input-helper-text');
  });

  test('does not render helper text when error is present', () => {
    render(
      <Input 
        id="test-input" 
        error="エラーメッセージ" 
        helperText="ヘルパーテキスト" 
      />
    );
    expect(screen.getByText('エラーメッセージ')).toBeInTheDocument();
    expect(screen.queryByText('ヘルパーテキスト')).not.toBeInTheDocument();
  });

  test('renders full width input', () => {
    render(<Input fullWidth data-testid="test-input" />);
    // 入力フィールド自体が w-full クラスを持っていることを確認
    expect(screen.getByTestId('test-input')).toHaveClass('w-full');
  });

  test('forwards ref to input element', () => {
    const ref = React.createRef<HTMLInputElement>();
    render(<Input ref={ref} data-testid="test-input" />);
    expect(ref.current).toBe(screen.getByTestId('test-input'));
  });

  test('passes additional props to input element', () => {
    render(
      <Input 
        type="email" 
        name="email" 
        required 
        disabled 
        data-testid="test-input" 
      />
    );
    const input = screen.getByTestId('test-input');
    expect(input).toHaveAttribute('type', 'email');
    expect(input).toHaveAttribute('name', 'email');
    expect(input).toHaveAttribute('required');
    expect(input).toBeDisabled();
  });
});
