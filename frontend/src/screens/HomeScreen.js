import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Row, Col } from 'react-bootstrap'
import Product from '../components/Product'
import Loader from '../components/Loader'
import Message from '../components/Message'
import Paginate from '../components/Paginate'
import { listProducts } from '../actions/productActions'
import { useNavigate, useLocation } from 'react-router-dom'
import ProductCarousel from '../components/ProductCarousel'
import { useLanguage } from '../i18n/LanguageContext'

function HomeScreen() {
  const navigate = useNavigate()
  const location = useLocation()
  const dispatch = useDispatch()
  const { t } = useLanguage()
  const productList = useSelector((state) => state.productList)
  const { error, loading, products, page, pages } = productList

  const currentPage = new URLSearchParams(location.search).get('page') || 1
  const keyword = new URLSearchParams(location.search).get('keyword') || ''

  useEffect(() => {
    dispatch(listProducts(keyword, currentPage))
  }, [dispatch, keyword, currentPage])


  return (
    <div>
      {!keyword && <ProductCarousel />}
      <h1>{t('sparePartsTitle')}</h1>
      {loading ? <Loader />
        : error ? <Message variant='danger'>{error}</Message>
          :
          <div>
            <Row>
              {products.map((product) => (
                <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
                  <Product product={product} />
                </Col>
              ))}
            </Row>
            <Paginate page={page} pages={pages} keyword={keyword} />
          </div>
      }
    </div>
  )
}

export default HomeScreen