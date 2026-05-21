import React, { useEffect } from 'react'
import { Link, useParams, useNavigate, useLocation } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { Row, Col, ListGroup, Image, Form, Button, Card } from 'react-bootstrap'
import Message from '../components/Message'
import { addToCart, removeFromCart } from '../actions/cartActions'
import { useLanguage } from '../i18n/LanguageContext'

function CartScreen() {
  const { id } = useParams()
  const navigate = useNavigate()
  const location = useLocation()
  const { t, formatPrice } = useLanguage()

  const productId = id
  const searchParams = new URLSearchParams(location.search)
  const qty = searchParams.has('qty') ? Number(searchParams.get('qty')) : 0

  const dispatch = useDispatch()

  const cart = useSelector(state => state.cart)
  const { cartItems } = cart

  useEffect(() => {
    if (productId) {
      dispatch(addToCart(productId, qty))
    }
  }, [dispatch, productId, qty])


  const removeFromCartHandler = (id) => {
    dispatch(removeFromCart(id))
  }

  const checkoutHandler = () => {
    navigate('/login?redirect=shipping')
  }

  return (
    <Row>
      <Col md={8}>
        <h1>{t('shoppingCart')}</h1>
        {cartItems.length === 0 ? (
          <Message variant='warning'>
            {t('cartEmpty')} <Link to='/'>{t('goBack')}</Link>
          </Message>
        ) : (
          <ListGroup>
            {cartItems.map(item => (
              <ListGroup.Item key={item.product}>
                <Row>
                  <Col md={2}>
                    <Image src={item.image} alt={item.name} fluid rounded />
                  </Col>

                  <Col md={3}>
                    <Link to={`/product/${item.product}`}>{item.name}</Link>
                  </Col>

                  <Col md={2}>
                    {formatPrice(item.price)}
                  </Col>

                  <Col md={3}>
                    <Form.Control
                      as="select"
                      value={item.qty}
                      onChange={(e) => dispatch(addToCart(item.product, Number(e.target.value)))}
                    >
                      {
                        [...Array(item.countInStock).keys()].map((x) => (
                          <option key={x + 1} value={x + 1}>
                            {x + 1}
                          </option>
                        ))
                      }
                    </Form.Control>
                  </Col>

                  <Col md={1}>
                    <Button
                      type='button'
                      variant='light'
                      onClick={() => removeFromCartHandler(item.product)}
                    >
                      <i className='fas fa-trash'></i>
                    </Button>
                  </Col>

                </Row>
              </ListGroup.Item>
            ))}
          </ListGroup>
        )}
      </Col>

      <Col md={4}>
        <Card>
          <ListGroup variant='flush'>
            <ListGroup.Item>
              <h2>{t('subtotal')} ({cartItems.reduce((acc, item) => acc + item.qty, 0)}) {t('items')}:</h2>
              {formatPrice(cartItems.reduce((acc, item) => acc + item.qty * item.price, 0))}
            </ListGroup.Item>
          </ListGroup>

          <ListGroup.Item className="d-flex justify-content-center align-items-center my-2">
            <Button
              type="button"
              className="btn-block"
              disabled={cartItems.length === 0}
              onClick={checkoutHandler}
            >
              {t('proceedToCheckout')}
            </Button>
          </ListGroup.Item>

        </Card>
      </Col>
    </Row>
  )
}

export default CartScreen