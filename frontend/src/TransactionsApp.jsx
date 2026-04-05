import { useState, useEffect } from 'react'

export default function TransactionsApp() {
  const [transactions, setTransactions] = useState([])

  useEffect(() => {
    fetch('/finance/api/transactions/')
      .then(res => res.json())
      .then(data => setTransactions(data))
  }, [])

  return (
    <div>
      <h2>My Transactions</h2>
      <ul>
        {transactions.map((t, i) => (
          <li key={i}>{t.date} — {t.category} — ${t.amount}</li>
        ))}
      </ul>
    </div>
  )
}