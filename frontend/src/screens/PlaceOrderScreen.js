import React, { useEffect } from 'react'
import { Button, Row, Col, ListGroup, Image, Card } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useNavigate } from 'react-router-dom'
import Message from '../components/Message'
import Loader from '../components/Loader'
import { createOrder } from '../actions/orderActions'
import { ORDER_CREATE_RESET } from '../constants/orderConstants'
import { useLanguage } from '../i18n/LanguageContext'

function PlaceOrderScreen() {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const { t, formatPrice } = useLanguage()

    const cart = useSelector(state => state.cart)
    const { cartItems, shippingAddress } = cart

    const orderCreate = useSelector(state => state.orderCreate)
    const { order, error, success, loading } = orderCreate

    const itemsPrice = cartItems.reduce((acc, item) => acc + item.qty * item.price, 0).toFixed(2)
    const shippingPrice = (Number(itemsPrice) > 2000 ? 0 : 150).toFixed(2)
    const totalPrice = (Number(itemsPrice) + Number(shippingPrice)).toFixed(2)

    useEffect(() => {
        if (success && order) {
            navigate(`/order/${order._id}`)
            dispatch({ type: ORDER_CREATE_RESET })
        }
    }, [success, order, navigate, dispatch])

    const placeOrder = () => {
        dispatch(createOrder({
            orderItems: cartItems,
            shippingAddress,
            totalPrice,
        }))
    }

    return (
        <div>
            <h1>{t('placeOrderTitle')}</h1>
            <Row>
                <Col md={8}>
                    <ListGroup variant='flush'>
                        <ListGroup.Item>
                            <h2>{t('shipping')}</h2>
                            <p>
                                <strong>{t('shippingAddress')}: </strong>
                                {shippingAddress.address}, {shippingAddress.city}{' '}
                                {shippingAddress.postalCode}, {shippingAddress.country}
                            </p>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h2>{t('orderItems')}</h2>
                            {cartItems.length === 0 ? (
                                <Message variant='warning'>{t('cartEmptyMsg')}</Message>
                            ) : (
                                <ListGroup variant='flush'>
                                    {cartItems.map((item, index) => (
                                        <ListGroup.Item key={index}>
                                            <Row>
                                                <Col md={1}>
                                                    <Image src={item.image} alt={item.name} fluid rounded />
                                                </Col>
                                                <Col>
                                                    <Link to={`/product/${item.product}`}>{item.name}</Link>
                                                </Col>
                                                <Col md={4}>
                                                    {item.qty} × {formatPrice(item.price)} = {formatPrice(item.qty * item.price)}
                                                </Col>
                                            </Row>
                                        </ListGroup.Item>
                                    ))}
                                </ListGroup>
                            )}
                        </ListGroup.Item>
                    </ListGroup>
                </Col>

                <Col md={4}>
                    <Card>
                        <ListGroup variant='flush'>
                            <ListGroup.Item>
                                <h2>{t('summary')}</h2>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col>{t('itemsPrice')}:</Col>
                                    <Col>{formatPrice(itemsPrice)}</Col>
                                </Row>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col>{t('shippingPrice')}:</Col>
                                    <Col>{Number(shippingPrice) === 0 ? t('free') : formatPrice(shippingPrice)}</Col>
                                </Row>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col><strong>{t('total')}:</strong></Col>
                                    <Col><strong>{formatPrice(totalPrice)}</strong></Col>
                                </Row>
                            </ListGroup.Item>

                            {error && (
                                <ListGroup.Item>
                                    <Message variant='danger'>{error}</Message>
                                </ListGroup.Item>
                            )}

                            <ListGroup.Item className="d-flex justify-content-center my-2">
                                {loading ? <Loader /> : (
                                    <Button
                                        type='button'
                                        className='btn-block'
                                        disabled={cartItems.length === 0}
                                        onClick={placeOrder}
                                    >
                                        {t('placeOrder')}
                                    </Button>
                                )}
                            </ListGroup.Item>
                        </ListGroup>
                    </Card>
                </Col>
            </Row>
        </div>
    )
}

export default PlaceOrderScreen
