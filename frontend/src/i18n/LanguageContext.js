import React, { createContext, useState, useEffect, useContext } from 'react'
import translations from './translations'

const LanguageContext = createContext()

const FALLBACK_RATE = 41.5 // fallback USD→UAH rate

export function LanguageProvider({ children }) {
    const [lang, setLang] = useState(
        localStorage.getItem('lang') || 'uk'
    )
    const [uahRate, setUahRate] = useState(() => {
        const cached = localStorage.getItem('uahRate')
        const cachedTime = localStorage.getItem('uahRateTime')
        // Use cached rate if less than 6 hours old
        if (cached && cachedTime && Date.now() - Number(cachedTime) < 6 * 3600 * 1000) {
            return Number(cached)
        }
        return FALLBACK_RATE
    })

    // Fetch live rate from National Bank of Ukraine API
    useEffect(() => {
        const cachedTime = localStorage.getItem('uahRateTime')
        if (cachedTime && Date.now() - Number(cachedTime) < 6 * 3600 * 1000) return

        fetch('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&json')
            .then(res => res.json())
            .then(data => {
                if (data && data[0] && data[0].rate) {
                    const rate = data[0].rate
                    setUahRate(rate)
                    localStorage.setItem('uahRate', String(rate))
                    localStorage.setItem('uahRateTime', String(Date.now()))
                }
            })
            .catch(() => {
                // silently use fallback
            })
    }, [])

    const switchLanguage = (newLang) => {
        setLang(newLang)
        localStorage.setItem('lang', newLang)
    }

    const t = (key) => {
        return translations[lang]?.[key] || translations['en']?.[key] || key
    }

    // Pick the right language field from a product object
    const p = (obj, field) => {
        if (!obj) return ''
        if (lang === 'en') {
            const enField = `${field}_en`
            return obj[enField] || obj[field] || ''
        }
        return obj[field] || ''
    }

    // Format price based on language: $123.00 (en) or 5 100 ₴ (uk)
    const formatPrice = (usdPrice) => {
        const num = Number(usdPrice) || 0
        if (lang === 'en') {
            return `$${num.toFixed(2)}`
        }
        const uah = Math.round(num * uahRate)
        return `${uah.toLocaleString('uk-UA')} ₴`
    }

    return (
        <LanguageContext.Provider value={{ lang, switchLanguage, t, p, formatPrice, uahRate }}>
            {children}
        </LanguageContext.Provider>
    )
}

export function useLanguage() {
    return useContext(LanguageContext)
}
