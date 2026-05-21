import React, { useState, useRef, useEffect } from 'react'
import './ChatWidget.css'

function ChatWidget() {
    const [isOpen, setIsOpen] = useState(false)
    const [messages, setMessages] = useState([
        {
            role: 'assistant',
            text: 'Вітаю! 👋 Я — ваш AI-консультант автозапчастин. Напишіть, яку деталь ви шукаєте.',
            products: [],
        },
    ])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const sendMessage = async () => {
        const trimmed = input.trim()
        if (!trimmed || loading) return

        const userMsg = { role: 'user', text: trimmed, products: [] }
        setMessages((prev) => [...prev, userMsg])
        setInput('')
        setLoading(true)

        try {
            const res = await fetch('/api/chat/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: trimmed }),
            })
            const data = await res.json()
            setMessages((prev) => [
                ...prev,
                {
                    role: 'assistant',
                    text: data.response || 'Вибачте, не вдалося отримати відповідь.',
                    products: data.products || [],
                    category: data.category || '',
                },
            ])
        } catch (err) {
            setMessages((prev) => [
                ...prev,
                {
                    role: 'assistant',
                    text: 'Помилка з\'єднання з сервером. Спробуйте пізніше.',
                    products: [],
                },
            ])
        } finally {
            setLoading(false)
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    }

    return (
        <>
            {/* Floating Action Button */}
            <button
                className={`chat-fab ${isOpen ? 'chat-fab--open' : ''}`}
                onClick={() => setIsOpen(!isOpen)}
                aria-label="Toggle chat"
            >
                {isOpen ? '✕' : '💬'}
            </button>

            {/* Chat Window */}
            {isOpen && (
                <div className="chat-window">
                    {/* Header */}
                    <div className="chat-header">
                        <div className="chat-header__dot" />
                        <span className="chat-header__title">AI Консультант</span>
                        <span className="chat-header__badge">RAG</span>
                    </div>

                    {/* Messages */}
                    <div className="chat-messages">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`chat-bubble chat-bubble--${msg.role}`}>
                                <p className="chat-bubble__text">{msg.text}</p>

                                {/* Product cards */}
                                {msg.products && msg.products.length > 0 && (
                                    <div className="chat-products">
                                        <p className="chat-products__label">
                                            🔎 Знайдено товарів: {msg.products.length}
                                            {msg.category ? ` (${msg.category})` : ''}
                                        </p>
                                        <div className="chat-products__grid">
                                            {msg.products.map((p) => (
                                                <a
                                                    key={p._id}
                                                    href={`/product/${p._id}`}
                                                    className="chat-product-card"
                                                >
                                                    <div className="chat-product-card__brand">{p.brand}</div>
                                                    <div className="chat-product-card__name">{p.name}</div>
                                                    <div className="chat-product-card__price">
                                                        {Number(p.price).toLocaleString('uk-UA')} ₴
                                                    </div>
                                                    <div className="chat-product-card__stock">
                                                        {p.countInStock > 0
                                                            ? `✅ В наявності (${p.countInStock})`
                                                            : '❌ Немає в наявності'}
                                                    </div>
                                                </a>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        ))}

                        {loading && (
                            <div className="chat-bubble chat-bubble--assistant">
                                <div className="chat-typing">
                                    <span /><span /><span />
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input */}
                    <div className="chat-input-bar">
                        <input
                            type="text"
                            className="chat-input"
                            placeholder="Напишіть запит..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            disabled={loading}
                        />
                        <button
                            className="chat-send-btn"
                            onClick={sendMessage}
                            disabled={loading || !input.trim()}
                        >
                            ➤
                        </button>
                    </div>
                </div>
            )}
        </>
    )
}

export default ChatWidget
