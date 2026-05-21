import React from 'react'
import { Card } from 'react-bootstrap'
import Rating from './Rating.js'
import { Link } from 'react-router-dom'
import { useLanguage } from '../i18n/LanguageContext'

function Product({ product }) {
  const { t, p, formatPrice } = useLanguage()

  return (
    <Card className="my-3 p-3 rounded">
      <Link to={`/product/${product._id}`}>
        <Card.Img src={product.image} />
      </Link>
      <Card.Body>
        <Link to={`/product/${product._id}`}>
          <Card.Title as="div">
            <strong>{p(product, 'name')}</strong>
          </Card.Title>
        </Link>

        <Card.Text as="div">
          <div className="my-3">
            <Rating value={product.rating} text={`${product.numReviews} ${t('reviews')}`} color={'#a86632'} />
          </div>
        </Card.Text>

        <Card.Text as="h3">
          {formatPrice(product.price)}
        </Card.Text>
      </Card.Body>
    </Card>
  )
}

export default Product