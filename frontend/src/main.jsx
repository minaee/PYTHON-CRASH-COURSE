import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import TransactionsApp from './TransactionsApp'

createRoot(document.getElementById('transactions-app')).render(
  <StrictMode>
    <TransactionsApp />
  </StrictMode>
)