import React from 'react'
import { Pagination } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'

function Paginate({ pages, page, keyword = '', isAdmin = false }) {
  let parsedKeyword = keyword;

  if (keyword && keyword.includes('?keyword=')) {
    parsedKeyword = keyword.split('?keyword=')[1].split('&')[0];
  }

  console.log('KEYWORD:', parsedKeyword);

  return (
    pages > 1 && (
      <Pagination>
        {[...Array(pages).keys()].map((x) => (
          <LinkContainer
            key={x + 1}
            to={{
              pathname: '/',
              search: `?keyword=${parsedKeyword}&page=${x + 1}`
            }}
          >
            <Pagination.Item
              active={x + 1 === page}
            >
              { x + 1 }
            </Pagination.Item>
          </LinkContainer>
        ))}
      </Pagination>
    )
  )
}

export default Paginate
