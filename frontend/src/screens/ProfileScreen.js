import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Form, Button, Row, Col, Table, Badge } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import Loader from '../components/Loader'
import Message from '../components/Message'
import { getUserDetails, updateUserProfile } from '../actions/userActions'
import { USER_UPDATE_PROFILE_RESET } from '../constants/userConstants'
import { useLanguage } from '../i18n/LanguageContext'
import axios from 'axios'

function ProfileScreen() {
    const navigate = useNavigate()
    const { t, formatPrice } = useLanguage()

    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [message, setMessage] = useState('')

    const [orders, setOrders] = useState([])
    const [loadingOrders, setLoadingOrders] = useState(true)
    const [errorOrders, setErrorOrders] = useState('')

    const dispatch = useDispatch()

    const userDetails = useSelector(state => state.userDetails)
    const { error, loading, user } = userDetails

    const userLogin = useSelector(state => state.userLogin)
    const { userInfo } = userLogin

    const userUpdateProfile = useSelector(state => state.userUpdateProfile)
    const { success } = userUpdateProfile

    const getEstimatedDelivery = (createdAt) => {
        const date = new Date(createdAt)
        date.setDate(date.getDate() + 4)
        return date.toLocaleDateString('uk-UA')
    }

    useEffect(() => {
        if (!userInfo) {
            navigate('/login')
        } else {
            if (!user || !user.name || success) {
                dispatch({ type: USER_UPDATE_PROFILE_RESET })
                dispatch(getUserDetails('profile'))
            } else {
                setName(user.name)
                setEmail(user.email)
            }

            const fetchOrders = async () => {
                try {
                    setLoadingOrders(true)
                    const config = {
                        headers: { Authorization: `Bearer ${userInfo.token}` }
                    }
                    const { data } = await axios.get('/api/orders/myorders/', config)
                    setOrders(data)
                    setLoadingOrders(false)
                } catch (err) {
                    setErrorOrders(err.response?.data?.detail || err.message)
                    setLoadingOrders(false)
                }
            }
            fetchOrders()
        }
    }, [dispatch, navigate, userInfo, user, success])

    const submitHandler = (e) => {
        e.preventDefault()
        if (password !== confirmPassword) {
            setMessage(t('passwordsDontMatch'))
        } else {
            dispatch(updateUserProfile({
                'id': user._id,
                'name': name,
                'email': email,
                'password': password,
            }))
            setMessage('')
        }
    }

    return (
        <Row>
            <Col md={3}>
                <h2>{t('profileTitle')}</h2>
                {message && <Message variant='danger'>{message}</Message>}
                {error && <Message variant='danger'>{error}</Message>}
                {loading && <Loader />}
                <Form onSubmit={submitHandler}>
                    <Form.Group controlId='name' className="mb-3">
                        <Form.Label>{t('name')}</Form.Label>
                        <Form.Control required type='name' placeholder={t('enterName')}
                            value={name} onChange={(e) => setName(e.target.value)} />
                    </Form.Group>

                    <Form.Group controlId='email' className="mb-3">
                        <Form.Label>{t('email')}</Form.Label>
                        <Form.Control required type='email' placeholder={t('enterEmail')}
                            value={email} onChange={(e) => setEmail(e.target.value)} />
                    </Form.Group>

                    <Form.Group controlId='password' className="mb-3">
                        <Form.Label>{t('password')}</Form.Label>
                        <Form.Control type='password' placeholder={t('newPassword')}
                            value={password} onChange={(e) => setPassword(e.target.value)} />
                    </Form.Group>

                    <Form.Group controlId='passwordConfirm' className="mb-3">
                        <Form.Label>{t('confirmPassword')}</Form.Label>
                        <Form.Control type='password' placeholder={t('confirmPassword')}
                            value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
                    </Form.Group>

                    <Button type='submit' variant='primary' className="mt-3">
                        {t('update')}
                    </Button>
                </Form>
            </Col>

            <Col md={9}>
                <h2>{t('myOrders')}</h2>
                {loadingOrders ? (
                    <Loader />
                ) : errorOrders ? (
                    <Message variant='danger'>{errorOrders}</Message>
                ) : orders.length === 0 ? (
                    <Message variant='info'>{t('noOrders')}</Message>
                ) : (
                    <Table striped bordered hover responsive className='table-sm'>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>{t('date')}</th>
                                <th>{t('amount')}</th>
                                <th>{t('payment')}</th>
                                <th>{t('estimatedDelivery')}</th>
                                <th>{t('statusCol')}</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {orders.map(order => (
                                <tr key={order._id}>
                                    <td>{order._id}</td>
                                    <td>{order.createdAt?.substring(0, 10)}</td>
                                    <td>{formatPrice(order.totalPrice)}</td>
                                    <td>
                                        {order.isPaid ? (
                                            <Badge bg='success'>✓ {order.paidAt?.substring(0, 10)}</Badge>
                                        ) : (
                                            <Badge bg='danger'>{t('notPaid')}</Badge>
                                        )}
                                    </td>
                                    <td>
                                        {order.isDelivered ? (
                                            <Badge bg='success'>✓ {t('delivered')}</Badge>
                                        ) : (
                                            <span>📦 {getEstimatedDelivery(order.createdAt)}</span>
                                        )}
                                    </td>
                                    <td>
                                        {(() => {
                                            const statusMap = {
                                                Processing: { bg: 'secondary', icon: '⏳', key: 'statusProcessing' },
                                                Shipped: { bg: 'info', icon: '🚚', key: 'statusShipped' },
                                                Delivered: { bg: 'success', icon: '✅', key: 'statusDelivered' },
                                                Returned: { bg: 'warning', icon: '↩️', key: 'statusReturned' },
                                                Lost: { bg: 'danger', icon: '❌', key: 'statusLost' },
                                            }
                                            const cfg = statusMap[order.status] || statusMap.Processing
                                            return <Badge bg={cfg.bg}>{cfg.icon} {t(cfg.key)}</Badge>
                                        })()}
                                    </td>
                                    <td>
                                        <Link to={`/order/${order._id}`}>
                                            <Button className='btn-sm' variant='light'>
                                                {t('details')}
                                            </Button>
                                        </Link>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </Table>
                )}
            </Col>
        </Row>
    )
}

export default ProfileScreen