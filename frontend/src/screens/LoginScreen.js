import React, { useState, useEffect } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { Form, Button, Row, Col } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import Loader from '../components/Loader'
import Message from '../components/Message'
import FormContainer from '../components/FormContainer'
import { login } from '../actions/userActions'
import { useLanguage } from '../i18n/LanguageContext'

function LoginScreen() {
  const navigate = useNavigate()
  const location = useLocation()
  const { t } = useLanguage()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const dispatch = useDispatch()

  const redirectRaw = location.search ? location.search.split('=')[1] : '/'
  const redirect = redirectRaw.startsWith('/') ? redirectRaw : `/${redirectRaw}`

  const userLogin = useSelector(state => state.userLogin)
  const { error, loading, userInfo } = userLogin

  useEffect(() => {
    if (userInfo) {
      navigate(redirect)
    }
  }, [navigate, userInfo, redirect])

  const submitHandler = (e) => {
    e.preventDefault()
    dispatch(login(email, password))
  }

  return (
    <FormContainer>
      <h1 className="mb-4">{t('signIn')}</h1>
      {error && <Message variant='danger'>{error}</Message>}
      {loading && <Loader />}
      <Form onSubmit={submitHandler}>

        <Form.Group controlId='email' className="mb-3">
          <Form.Label>{t('email')}</Form.Label>
          <Form.Control
            type='email'
            placeholder={t('enterEmail')}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </Form.Group>

        <Form.Group controlId='password' className="mb-3">
          <Form.Label>{t('password')}</Form.Label>
          <Form.Control
            type='password'
            placeholder={t('enterPassword')}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Group>

        <Button type='submit' variant='primary' className="mt-3">
          {t('signIn')}
        </Button>
      </Form>

      <Row className="py-3">
        <Col>
          {t('newCustomer')} <Link
            to={redirect ? `/register?redirect=${redirect}` : '/register'}>
            {t('register')}
          </Link>
        </Col>
      </Row>
    </FormContainer>
  )
}

export default LoginScreen