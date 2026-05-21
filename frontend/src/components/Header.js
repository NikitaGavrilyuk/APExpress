import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Navbar, Nav, Container, NavDropdown } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import SearchBox from './SearchBox'
import { logout } from '../actions/userActions'
import { useLanguage } from '../i18n/LanguageContext'

function Header() {

  const userLogin = useSelector(state => state.userLogin)
  const { userInfo } = userLogin

  const dispatch = useDispatch()
  const { lang, switchLanguage, t } = useLanguage()

  const logoutHandler = () => {
    dispatch(logout())
  }

  return (
    <header>
      <Navbar bg="danger" variant="dark" expand="lg" collapseOnSelect>
        <Container>
          <LinkContainer to='/'>
            <Navbar.Brand className="d-flex align-items-center">
              <img
                src="/logo.png"
                alt="Logo"
                width="40"
                height="40"
                className="d-inline-block align-top me-2"
              />
              APExpress
            </Navbar.Brand>
          </LinkContainer>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <SearchBox />
            <Nav className="ms-auto">

              <LinkContainer to='/cart'>
                <Nav.Link><i className="fas fa-shopping-cart"></i> {t('cart')}</Nav.Link>
              </LinkContainer>

              {userInfo ? (
                <NavDropdown title={userInfo.name} id='username'>
                  <LinkContainer to='/profile'>
                    <NavDropdown.Item>{t('profile')}</NavDropdown.Item>
                  </LinkContainer>

                  <NavDropdown.Item onClick={logoutHandler}>{t('logout')}</NavDropdown.Item>

                </NavDropdown>
              ) : (
                <LinkContainer to='/login'>
                  <Nav.Link><i className="fas fa-user"></i> {t('login')}</Nav.Link>
                </LinkContainer>
              )}

              {/* Language Switcher */}
              <NavDropdown title={lang === 'uk' ? '🇺🇦 UA' : '🇬🇧 EN'} id='language-switcher'>
                <NavDropdown.Item
                  onClick={() => switchLanguage('uk')}
                  active={lang === 'uk'}
                >
                  🇺🇦 Українська
                </NavDropdown.Item>
                <NavDropdown.Item
                  onClick={() => switchLanguage('en')}
                  active={lang === 'en'}
                >
                  🇬🇧 English
                </NavDropdown.Item>
              </NavDropdown>

            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
}

export default Header;
