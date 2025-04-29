import React from 'react';
import { render, screen } from '@testing-library/react';
import { Select } from '../../components/common/Select';

describe('Select Component', () => {
  const options = [
    { value: 'option1', label: 'オプション1' },
    { value: 'option2', label: 'オプション2' },
    { value: 'option3', label: 'オプション3' },
  ];

  test('renders select element', () => {
    render(<Select options={options} data-testid="test-select" />);
    const select = screen.getByTestId('test-select');
    expect(select).toBeInTheDocument();
    expect(select.tagName).toBe('SELECT');
  });

  test('renders with label', () => {
    render(<Select id="test-select" label="テストラベル" options={options} />);
    const label = screen.getByText('テストラベル');
    expect(label).toBeInTheDocument();
    expect(label.tagName).toBe('LABEL');
    expect(label).toHaveAttribute('for', 'test-select');
  });

  test('renders with options', () => {
    render(<Select options={options} />);
    options.forEach(option => {
      const optionElement = screen.getByText(option.label);
      expect(optionElement).toBeInTheDocument();
      expect(optionElement.tagName).toBe('OPTION');
      expect(optionElement).toHaveAttribute('value', option.value);
    });
  });

  test('renders with placeholder', () => {
    render(<Select options={options} placeholder="選択してください" />);
    const placeholderOption = screen.getByText('選択してください');
    expect(placeholderOption).toBeInTheDocument();
    expect(placeholderOption.tagName).toBe('OPTION');
    expect(placeholderOption).toHaveAttribute('value', '');
    expect(placeholderOption).toHaveAttribute('disabled');
  });

  test('renders with error message', () => {
    render(<Select id="test-select" error="エラーメッセージ" options={options} />);
    const errorMessage = screen.getByText('エラーメッセージ');
    expect(errorMessage).toBeInTheDocument();
    expect(errorMessage).toHaveAttribute('id', 'test-select-error');
    
    const select = screen.getByRole('combobox');
    expect(select).toHaveAttribute('aria-invalid', 'true');
    expect(select).toHaveClass('border-red-500');
  });

  test('renders with helper text', () => {
    render(<Select id="test-select" helperText="ヘルパーテキスト" options={options} />);
    const helperText = screen.getByText('ヘルパーテキスト');
    expect(helperText).toBeInTheDocument();
    expect(helperText).toHaveAttribute('id', 'test-select-helper-text');
  });

  test('does not render helper text when error is present', () => {
    render(
      <Select 
        id="test-select" 
        error="エラーメッセージ" 
        helperText="ヘルパーテキスト" 
        options={options}
      />
    );
    expect(screen.getByText('エラーメッセージ')).toBeInTheDocument();
    expect(screen.queryByText('ヘルパーテキスト')).not.toBeInTheDocument();
  });

  test('renders full width select', () => {
    render(<Select fullWidth options={options} data-testid="test-select" />);
    expect(screen.getByTestId('test-select')).toHaveClass('w-full');
  });

  test('forwards ref to select element', () => {
    const ref = React.createRef<HTMLSelectElement>();
    render(<Select ref={ref} options={options} data-testid="test-select" />);
    expect(ref.current).toBe(screen.getByTestId('test-select'));
  });

  test('passes additional props to select element', () => {
    render(
      <Select 
        name="category" 
        required 
        disabled 
        data-testid="test-select" 
        options={options}
      />
    );
    const select = screen.getByTestId('test-select');
    expect(select).toHaveAttribute('name', 'category');
    expect(select).toHaveAttribute('required');
    expect(select).toBeDisabled();
  });
});
