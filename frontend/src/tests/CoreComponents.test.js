import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { legacy_createStore as createStore, applyMiddleware } from 'redux';
import { thunk } from 'redux-thunk';
import { LanguageProvider } from '../i18n/LanguageContext';
import Product from '../components/Product';
import ChatWidget from '../components/ChatWidget';
import ProductScreen from '../screens/ProductScreen';

// Спрощений мок Redux-сховища для тестів з підтримкою thunk
const initialState = {
    productDetails: { product: { _id: '1', name: 'Гальмівні колодки', price: 500, countInStock: 5, reviews: [] }, loading: false, error: null },
    userLogin: { userInfo: null },
    productReviewCreate: { success: false, error: null }
};

const mockStore = createStore(
    (state = initialState) => state,
    applyMiddleware(thunk)
);

// Мокаємо хуки роутера
jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => jest.fn(),
    useParams: () => ({ id: '1' })
}));

describe('APExpress Core Components', () => {
    
    test('1. Рендеринг картки товару', () => {
        const product = { _id: '1', name: 'Моторне мастило', price: 800, rating: 5, numReviews: 2 };
        render(
            <MemoryRouter>
                <LanguageProvider>
                    <Product product={product} />
                </LanguageProvider>
            </MemoryRouter>
        );
        expect(screen.getByText(/Моторне мастило/i)).toBeInTheDocument();
    });

    test('2. Відображення повідомлення в AI-чаті', () => {
        render(<ChatWidget />);
        
        // Відкриваємо віджет
        const toggleBtn = screen.getByLabelText(/Toggle chat/i);
        fireEvent.click(toggleBtn);
        
        // Перевіряємо вітальне повідомлення
        expect(screen.getByText(/Я — ваш AI-консультант/i)).toBeInTheDocument();
    });

    test('3. Функціонування кнопки додавання в кошик', () => {
        render(
            <Provider store={mockStore}>
                <MemoryRouter>
                    <LanguageProvider>
                        <ProductScreen />
                    </LanguageProvider>
                </MemoryRouter>
            </Provider>
        );
        
        // Знаходимо всі кнопки на сторінці та беремо кнопку додавання (остання або за атрибутами)
        const buttons = screen.getAllByRole('button');
        const addToCartBtn = buttons.find(b => b.textContent.match(/(addToCart|Додати в кошик)/i) || !b.disabled);
        
        expect(addToCartBtn).toBeInTheDocument();
        expect(addToCartBtn).not.toBeDisabled();
    });
});
