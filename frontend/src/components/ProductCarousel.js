import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link } from 'react-router-dom'
import { Carousel, Image } from 'react-bootstrap'
import Loader from './Loader'
import Message from './Message'
import { listTopProducts } from '../actions/productActions'
import { useLanguage } from '../i18n/LanguageContext'


function ProductCarousel() {
  const dispatch = useDispatch()
  const { p, formatPrice } = useLanguage()
  const productTopRated = useSelector(state => state.productTopRated)
  const { error, loading, products } = productTopRated

  useEffect(() => {
    dispatch(listTopProducts())
  }, [dispatch])

  return (loading ? <Loader />
    : error
      ? <Message variant='danger'>{error}</Message>
      : (
        <Carousel pause='hover' className='carousel'>
          {products.map(product => (
            <Carousel.Item key={product._id}>
              <Link to={`/product/${product._id}`}>
                <Image src={product.image} alt={p(product, 'name')} fluid />
                <Carousel.Caption className='carousel.caption'>
                  <h4>{p(product, 'name')} ({formatPrice(product.price)})</h4>
                </Carousel.Caption>
              </Link>
            </Carousel.Item>
          ))}
        </Carousel>
      )
  )
}

export default ProductCarousel