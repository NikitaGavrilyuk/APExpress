import React, { useEffect } from 'react'
import { Row, Col, ListGroup, Image, Card, Button, Badge } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useParams } from 'react-router-dom'
import Message from '../components/Message'
import Loader from '../components/Loader'
import { getOrderDetails, payOrder } from '../actions/orderActions'
import { ORDER_PAY_RESET } from '../constants/orderConstants'
import { useLanguage } from '../i18n/LanguageContext'

function OrderScreen() {
    const { id } = useParams()
    const dispatch = useDispatch()
    const { t, formatPrice } = useLanguage()

    const orderDetails = useSelector(state => state.orderDetails)
    const { order, error, loading } = orderDetails

    const orderPay = useSelector(state => state.orderPay)
    const { loading: loadingPay, success: successPay } = orderPay

    useEffect(() => {
        if (successPay) {
            dispatch({ type: ORDER_PAY_RESET })
        }
        dispatch(getOrderDetails(id))
    }, [dispatch, id, successPay])

    const handleMockPayment = () => {
        dispatch(payOrder(id))
    }

    const STATUS_CONFIG = {
        Processing: { bg: 'secondary', icon: '⏳', key: 'statusProcessing' },
        Shipped: { bg: 'info', icon: '🚚', key: 'statusShipped' },
        Delivered: { bg: 'success', icon: '✅', key: 'statusDelivered' },
        Returned: { bg: 'warning', icon: '↩️', key: 'statusReturned' },
        Lost: { bg: 'danger', icon: '❌', key: 'statusLost' },
    }

    const getStatusBadge = (status) => {
        const config = STATUS_CONFIG[status] || STATUS_CONFIG.Processing
        return (
            <Badge bg={config.bg} className='px-3 py-2' style={{ fontSize: '0.9rem' }}>
                {config.icon} {t(config.key)}
            </Badge>
        )
    }

    return loading ? (
        <Loader />
    ) : error ? (
        <Message variant='danger'>{error}</Message>
    ) : order && (
        <div>
            <h1>{t('orderNumber')} #{order._id}</h1>
            <Row>
                <Col md={8}>
                    <ListGroup variant='flush'>
                        <ListGroup.Item>
                            <h2>{t('shipping')}</h2>
                            <p><strong>{t('client')}: </strong>{order.user?.name}</p>
                            <p><strong>Email: </strong>{order.user?.email}</p>
                            <p>
                                <strong>{t('shippingAddress')}: </strong>
                                {order.shippingAddress?.address}, {order.shippingAddress?.city}{' '}
                                {order.shippingAddress?.postalCode}, {order.shippingAddress?.country}
                            </p>
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h2>{t('orderStatus')}</h2>
                            {getStatusBadge(order.status)}
                            {order.isDelivered && order.deliveredAt && (
                                <span className='ms-2 text-muted'>
                                    ({order.deliveredAt?.substring(0, 10)})
                                </span>
                            )}
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h2>{t('payment')}</h2>
                            {order.isPaid ? (
                                <Message variant='success'>
                                    <Badge bg='success' className='me-2'>✓ {t('paid')}</Badge>
                                    {order.paidAt?.substring(0, 10)}
                                </Message>
                            ) : (
                                <Message variant='danger'>{t('notPaid')}</Message>
                            )}
                        </ListGroup.Item>

                        <ListGroup.Item>
                            <h2>{t('orderItems')}</h2>
                            <ListGroup variant='flush'>
                                {order.orderItems?.map((item, index) => (
                                    <ListGroup.Item key={index}>
                                        <Row>
                                            <Col md={1}>
                                                <Image src={item.image} alt={item.name} fluid rounded />
                                            </Col>
                                            <Col>
                                                <Link to={`/product/${item.product}`}>{item.name}</Link>
                                            </Col>
                                            <Col md={4}>
                                                {item.qty} × {formatPrice(item.price)} = {formatPrice(item.qty * Number(item.price))}
                                            </Col>
                                        </Row>
                                    </ListGroup.Item>
                                ))}
                            </ListGroup>
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
                                    <Col>
                                        {formatPrice(order.orderItems?.reduce((acc, item) => acc + item.qty * Number(item.price), 0))}
                                    </Col>
                                </Row>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col>{t('shippingPrice')}:</Col>
                                    <Col>
                                        {Number(order.shippingPrice) === 0 ? t('free') : formatPrice(order.shippingPrice)}
                                    </Col>
                                </Row>
                            </ListGroup.Item>

                            <ListGroup.Item>
                                <Row>
                                    <Col><strong>{t('total')}:</strong></Col>
                                    <Col><strong>{formatPrice(order.totalPrice)}</strong></Col>
                                </Row>
                            </ListGroup.Item>

                            {!order.isPaid && (
                                <ListGroup.Item className="d-flex justify-content-center my-2">
                                    {loadingPay ? <Loader /> : (
                                        <Button
                                            type='button'
                                            className='btn-block btn-success'
                                            onClick={handleMockPayment}
                                        >
                                            {t('payOrder')}
                                        </Button>
                                    )}
                                </ListGroup.Item>
                            )}
                        </ListGroup>
                    </Card>
                </Col>
            </Row>
        </div>
    )
}

export default OrderScreen
