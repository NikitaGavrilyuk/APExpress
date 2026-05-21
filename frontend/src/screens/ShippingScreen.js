import React, { useState, useEffect } from 'react'
import { Form, Button } from 'react-bootstrap'
import { useDispatch, useSelector } from 'react-redux'
import FormContainer from '../components/FormContainer'
import { useNavigate } from 'react-router-dom'
import { saveShippingAddress } from '../actions/cartActions'
import { useLanguage } from '../i18n/LanguageContext'
import axios from 'axios'

function ShippingScreen() {
  const { shippingAddress } = useSelector(state => state.cart)
  const { t } = useLanguage()

  const [address, setAddress] = useState(shippingAddress.address || '')
  const [city, setCity] = useState(shippingAddress.city || '')
  const [postalCode, setPostalCode] = useState(shippingAddress.postalCode || '')
  const [country, setCountry] = useState(shippingAddress.country || 'Україна')

  const [branches, setBranches] = useState([])
  const [selectedBranch, setSelectedBranch] = useState('')

  const dispatch = useDispatch()
  const navigate = useNavigate()

  useEffect(() => {
    const fetchBranches = async () => {
      const { data } = await axios.get('/api/orders/delivery-branches/')
      setBranches(data)
    }
    fetchBranches()
  }, [])

  const filteredBranches = city
    ? branches.filter(b => b.city.toLowerCase() === city.toLowerCase())
    : branches

  const handleBranchSelect = (e) => {
    const branch = branches.find(b => b.id === Number(e.target.value))
    if (branch) {
      setSelectedBranch(branch.id)
      setCity(branch.city)
      setAddress(branch.branch)
    }
  }

  const submitHandler = (e) => {
    e.preventDefault()
    dispatch(saveShippingAddress({ address, city, postalCode, country }))
    navigate('/placeorder')
  }

  return (
    <FormContainer>
      <h1>{t('shipping')}</h1>

      <Form onSubmit={submitHandler}>
        <Form.Group controlId='country' className="mb-3">
          <Form.Label>{t('country')}</Form.Label>
          <Form.Control required type='text' placeholder={t('enterCountry')}
            value={country} onChange={(e) => setCountry(e.target.value)} />
        </Form.Group>

        <Form.Group controlId='city' className="mb-3">
          <Form.Label>{t('city')}</Form.Label>
          <Form.Control required type='text' placeholder={t('enterCity')}
            value={city} onChange={(e) => setCity(e.target.value)} />
        </Form.Group>

        <Form.Group controlId='branch' className="mb-3">
          <Form.Label>{t('novaPoshtaBranch')}</Form.Label>
          <Form.Control as='select' value={selectedBranch} onChange={handleBranchSelect}>
            <option value=''>{t('selectBranch')}</option>
            {filteredBranches.map(b => (
              <option key={b.id} value={b.id}>{b.city} — {b.branch}</option>
            ))}
          </Form.Control>
        </Form.Group>

        <Form.Group controlId='address' className="mb-3">
          <Form.Label>{t('address')}</Form.Label>
          <Form.Control required type='text' placeholder={t('enterAddress')}
            value={address} onChange={(e) => setAddress(e.target.value)} />
        </Form.Group>

        <Form.Group controlId='postalCode' className="mb-3">
          <Form.Label>{t('postalCode')}</Form.Label>
          <Form.Control required type='text' placeholder={t('enterPostalCode')}
            value={postalCode} onChange={(e) => setPostalCode(e.target.value)} />
        </Form.Group>

        <Button type='submit' variant='primary' className='mt-2'>
          {t('continue')}
        </Button>
      </Form>
    </FormContainer>
  )
}

export default ShippingScreen
