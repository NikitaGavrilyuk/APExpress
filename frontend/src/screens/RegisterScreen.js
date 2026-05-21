import React, { useState, useEffect } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { Form, Button, Row, Col } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import Loader from '../components/Loader'
import Message from '../components/Message'
import FormContainer from '../components/FormContainer'
import { register } from '../actions/userActions'
import { useLanguage } from '../i18n/LanguageContext'

function RegisterScreen() {
        const navigate = useNavigate()
        const location = useLocation()
        const { t } = useLanguage()

        const [name, setName] = useState('')
        const [email, setEmail] = useState('')
        const [password, setPassword] = useState('')
        const [confirmPassword, setConfirmPassword] = useState('')
        const [message, setMessage] = useState('')

        const dispatch = useDispatch()

        const redirectRaw = location.search ? location.search.split('=')[1] : '/'
        const redirect = redirectRaw.startsWith('/') ? redirectRaw : `/${redirectRaw}`

        const userRegister = useSelector(state => state.userRegister)
        const { error, loading, userInfo } = userRegister

        useEffect(() => {
                if (userInfo) {
                        navigate(redirect)
                }
        }, [navigate, userInfo, redirect])

        const submitHandler = (e) => {
                e.preventDefault()
                if (password !== confirmPassword) {
                        setMessage(t('passwordsDontMatch'))
                } else {
                        dispatch(register(name, email, password))
                }
        }

        return (
                <FormContainer>
                        <h1 className="mb-4">{t('register')}</h1>
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
                                        <Form.Control required type='password' placeholder={t('enterPassword')}
                                                value={password} onChange={(e) => setPassword(e.target.value)} />
                                </Form.Group>

                                <Form.Group controlId='passwordConfirm' className="mb-3">
                                        <Form.Label>{t('confirmPassword')}</Form.Label>
                                        <Form.Control required type='password' placeholder={t('confirmPassword')}
                                                value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
                                </Form.Group>

                                <Button type='submit' variant='primary' className="mt-3">
                                        {t('register')}
                                </Button>
                        </Form>

                        <Row className="py-3">
                                <Col>
                                        {t('haveAccount')} <Link
                                                to={redirect ? `/login?redirect=${redirect}` : '/login'}>
                                                {t('signIn')}
                                        </Link>
                                </Col>
                        </Row>
                </FormContainer>
        )
}

export default RegisterScreen