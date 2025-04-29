import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Pagination } from '../../components/common/Pagination';

describe('Pagination Component', () => {
  const onPageChangeMock = jest.fn();

  beforeEach(() => {
    onPageChangeMock.mockClear();
  });

  test('renders nothing when totalPages is 1', () => {
    render(
      <Pagination currentPage={1} totalPages={1} onPageChange={onPageChangeMock} />
    );
    expect(screen.queryByRole('navigation')).not.toBeInTheDocument();
  });

  test('renders pagination with correct number of pages', () => {
    render(
      <Pagination currentPage={3} totalPages={5} onPageChange={onPageChangeMock} />
    );
    
    // 前後のナビゲーションボタンと5つのページボタン、最初と最後のボタン
    expect(screen.getAllByRole('button')).toHaveLength(9);
    
    // 現在のページが強調表示されていることを確認
    const currentPageButton = screen.getByRole('button', { current: 'page' });
    expect(currentPageButton).toHaveTextContent('3');
  });

  test('disables previous buttons when on first page', () => {
    render(
      <Pagination currentPage={1} totalPages={5} onPageChange={onPageChangeMock} />
    );
    
    const firstPageButton = screen.getByLabelText('最初のページへ');
    const prevPageButton = screen.getByLabelText('前のページへ');
    
    expect(firstPageButton).toBeDisabled();
    expect(prevPageButton).toBeDisabled();
  });

  test('disables next buttons when on last page', () => {
    render(
      <Pagination currentPage={5} totalPages={5} onPageChange={onPageChangeMock} />
    );
    
    const lastPageButton = screen.getByLabelText('最後のページへ');
    const nextPageButton = screen.getByLabelText('次のページへ');
    
    expect(lastPageButton).toBeDisabled();
    expect(nextPageButton).toBeDisabled();
  });

  test('calls onPageChange with correct page number when page button is clicked', () => {
    render(
      <Pagination currentPage={3} totalPages={5} onPageChange={onPageChangeMock} />
    );
    
    const pageButton = screen.getByLabelText('2ページ目へ');
    fireEvent.click(pageButton);
    
    expect(onPageChangeMock).toHaveBeenCalledWith(2);
  });

  test('calls onPageChange with correct page number when next button is clicked', () => {
    render(
      <Pagination currentPage={3} totalPages={5} onPageChange={onPageChangeMock} />
    );
    
    const nextButton = screen.getByLabelText('次のページへ');
    fireEvent.click(nextButton);
    
    expect(onPageChangeMock).toHaveBeenCalledWith(4);
  });

  test('calls onPageChange with correct page number when previous button is clicked', () => {
    render(
      <Pagination currentPage={3} totalPages={5} onPageChange={onPageChangeMock} />
    );
    
    const prevButton = screen.getByLabelText('前のページへ');
    fireEvent.click(prevButton);
    
    expect(onPageChangeMock).toHaveBeenCalledWith(2);
  });

  test('does not call onPageChange when clicking on current page', () => {
    render(
      <Pagination currentPage={3} totalPages={5} onPageChange={onPageChangeMock} />
    );
    
    const currentPageButton = screen.getByRole('button', { current: 'page' });
    fireEvent.click(currentPageButton);
    
    expect(onPageChangeMock).not.toHaveBeenCalled();
  });

  test('renders with ellipsis for many pages', () => {
    render(
      <Pagination currentPage={5} totalPages={10} onPageChange={onPageChangeMock} maxVisiblePages={3} />
    );
    
    // 省略記号が表示されていることを確認
    const ellipses = screen.getAllByText('...');
    expect(ellipses).toHaveLength(2);
    
    // 最初と最後のページボタンが表示されていることを確認
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('10')).toBeInTheDocument();
  });

  test('hides first/last buttons when showFirstLastButtons is false', () => {
    render(
      <Pagination 
        currentPage={3} 
        totalPages={5} 
        onPageChange={onPageChangeMock} 
        showFirstLastButtons={false} 
      />
    );
    
    expect(screen.queryByLabelText('最初のページへ')).not.toBeInTheDocument();
    expect(screen.queryByLabelText('最後のページへ')).not.toBeInTheDocument();
  });

  test('applies custom className', () => {
    render(
      <Pagination 
        currentPage={3} 
        totalPages={5} 
        onPageChange={onPageChangeMock} 
        className="custom-pagination" 
      />
    );
    
    const nav = screen.getByRole('navigation');
    expect(nav).toHaveClass('custom-pagination');
  });
});
