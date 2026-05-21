import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { Row, Col, Image, ListGroup, Button, Card, Form } from 'react-bootstrap'
import Rating from '../components/Rating'
import Loader from '../components/Loader'
import Message from '../components/Message'
import { listProductDetails, createProductReview } from '../actions/productActions'
import { PRODUCT_CREATE_REVIEW_RESET } from '../constants/productConstants'
import { useLanguage } from '../i18n/LanguageContext'

function ProductScreen() {
    const [qty, setQty] = useState(1)
    const [rating, setRating] = useState(0)
    const [comment, setComment] = useState('')

    const navigate = useNavigate()
    const { t, p, formatPrice } = useLanguage()

    const dispatch = useDispatch()
    const productDetails = useSelector((state) => state.productDetails)
    const { loading, error, product } = productDetails

    const userLogin = useSelector((state) => state.userLogin)
    const { userInfo } = userLogin

    const productReviewCreate = useSelector((state) => state.productReviewCreate)
    const {
        loading: loadingProductReview,
        error: errorProductReview,
        success: successProductReview,
    } = productReviewCreate

    const { id } = useParams()

    useEffect(() => {
        if (successProductReview) {
            setRating(0)
            setComment('')
            const timer = setTimeout(() => {
                dispatch({ type: PRODUCT_CREATE_REVIEW_RESET })
            }, 3000)
            return () => clearTimeout(timer)
        }

        if (errorProductReview) {
            const errorTimer = setTimeout(() => {
                dispatch({ type: PRODUCT_CREATE_REVIEW_RESET })
            }, 3000)

            return () => clearTimeout(errorTimer)
        }

        dispatch(listProductDetails(id))

    }, [dispatch, id, successProductReview, errorProductReview])

    const addToCartHandler = () => {
        navigate(`/cart/${id}?qty=${qty}`)
    }

    const submitHandler = (e) => {
        e.preventDefault()
        dispatch(createProductReview(id, { rating, comment }))
    }

    return (
        <div>
            <Link to='/' className='btn btn-light my-3'>{t('goBack')}</Link>
            {loading ?
                <Loader />
                : error
                    ? <Message variant='danger'>{error}</Message>
                    : (
                        <div>
                            <Row>
                                <Col md={6}>
                                    <Image src={product.image} alt={p(product, 'name')} fluid />
                                </Col>

                                <Col md={3}>
                                    <ListGroup variant="flush">
                                        <ListGroup.Item>
                                            <h3>{p(product, 'name')}</h3>
                                        </ListGroup.Item>

                                        <ListGroup.Item>
                                            <Rating value={product.rating} text={`${product.numReviews} ${t('reviews')}`} color={'#a86632'} />
                                        </ListGroup.Item>

                                        <ListGroup.Item>
                                            {t('price')}: {formatPrice(product.price)}
                                        </ListGroup.Item>

                                        <ListGroup.Item>
                                            {t('description')}: {p(product, 'description')}
                                        </ListGroup.Item>
                                    </ListGroup>
                                </Col>

                                <Col md={3}>
                                    <Card>
                                        <ListGroup variant="flush">
                                            <ListGroup.Item>
                                                <Row>
                                                    <Col>{t('price')}:</Col>
                                                    <Col>
                                                        <strong>{formatPrice(product.price)}</strong>
                                                    </Col>
                                                </Row>
                                            </ListGroup.Item>

                                            <ListGroup.Item>
                                                <Row>
                                                    <Col>{t('status')}:</Col>
                                                    <Col>
                                                        {product.countInStock > 0 ? t('inStock') : t('outOfStock')}
                                                    </Col>
                                                </Row>
                                            </ListGroup.Item>

                                            {product.countInStock > 0 && (
                                                <ListGroup.Item>
                                                    <Row>
                                                        <Col>{t('qty')}:</Col>
                                                        <Col xs='auto' className='my-1'>
                                                            <Form.Control
                                                                as="select"
                                                                value={qty}
                                                                onChange={(e) => setQty(e.target.value)}
                                                            >
                                                                {
                                                                    [...Array(product.countInStock).keys()].map((x) => (
                                                                        <option key={x + 1} value={x + 1}>
                                                                            {x + 1}
                                                                        </option>
                                                                    ))
                                                                }
                                                            </Form.Control>
                                                        </Col>
                                                    </Row>
                                                </ListGroup.Item>
                                            )}

                                            <ListGroup.Item>
                                                <Button
                                                    onClick={addToCartHandler}
                                                    className='btn-block'
                                                    disabled={product.countInStock === 0}
                                                    type='button'>
                                                    {t('addToCart')}
                                                </Button>
                                            </ListGroup.Item>
                                        </ListGroup>
                                    </Card>
                                </Col>
                            </Row>

                            <Row>
                                <Col md={6}>
                                    <h4>{t('reviews')}</h4>
                                    {product.reviews.length === 0 && <Message variant='primary'>{t('reviews')}: 0</Message>}
                                    <ListGroup variant='flush'>
                                        {product.reviews.map((review) => (
                                            <ListGroup.Item key={review._id}>
                                                <strong>{review.name}</strong>
                                                <Rating value={review.rating} color='#d9a668' />
                                                <p>{review.createdAt.substring(0, 10)}</p>
                                                <p>{review.comment}</p>
                                            </ListGroup.Item>
                                        ))}

                                        <ListGroup.Item>
                                            <h4>{t('writeReview')}</h4>

                                            {loadingProductReview && <Loader />}
                                            {successProductReview && <Message variant='success'>✓</Message>}
                                            {errorProductReview && <Message variant='danger'>{errorProductReview}</Message>}

                                            {userInfo ? (
                                                <Form onSubmit={submitHandler}>
                                                    <Form.Group controlId='rating'>
                                                        <Form.Label className='mt-2'>{t('rating')}</Form.Label>
                                                        <Form.Control
                                                            as='select'
                                                            value={rating}
                                                            onChange={(e) => setRating(e.target.value)}
                                                        >
                                                            <option value=''>{t('selectRating')}</option>
                                                            <option value='1'>1 - {t('poor')}</option>
                                                            <option value='2'>2 - {t('below_average')}</option>
                                                            <option value='3'>3 - {t('average')}</option>
                                                            <option value='4'>4 - {t('good')}</option>
                                                            <option value='5'>5 - {t('excellent')}</option>
                                                        </Form.Control>
                                                    </Form.Group>

                                                    <Form.Group controlId='comment'>
                                                        <Form.Label className='mt-2'>{t('comment')}</Form.Label>
                                                        <Form.Control
                                                            as='textarea'
                                                            row='5'
                                                            value={comment}
                                                            onChange={(e) => setComment(e.target.value)}
                                                            className='mb-2'
                                                        >

                                                        </Form.Control>
                                                    </Form.Group>

                                                    <Button
                                                        disabled={loadingProductReview}
                                                        type='submit'
                                                        variant='primary'
                                                        className='mt-2'
                                                    >
                                                        {t('submitReview')}
                                                    </Button>

                                                </Form>
                                            ) : (
                                                <Message variant='info'>
                                                    <Link to='/login'>{t('signIn')}</Link>
                                                </Message>
                                            )}
                                        </ListGroup.Item>
                                    </ListGroup>
                                </Col>
                            </Row>
                        </div>
                    )
            }
        </div>
    )
}

export default ProductScreen;
