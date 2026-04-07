import { useState, useEffect } from 'react'
import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from 'recharts'

const EMPTY_FORM = { date: '', amount: '', category: '', description: '', type: 'expense' }
const COLORS = ['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6', '#8b5cf6', '#ec4899']

function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

function SummaryCards({ income, expenses, net }) {
  return (
    <div className="row mb-4">
      <div className="col-md-4">
        <div className="card text-white bg-success mb-3">
          <div className="card-body">
            <h6 className="card-title">Total Income</h6>
            <h3>${income.toFixed(2)}</h3>
          </div>
        </div>
      </div>
      <div className="col-md-4">
        <div className="card text-white bg-danger mb-3">
          <div className="card-body">
            <h6 className="card-title">Total Expenses</h6>
            <h3>${expenses.toFixed(2)}</h3>
          </div>
        </div>
      </div>
      <div className="col-md-4">
        <div className={`card text-white mb-3 ${net >= 0 ? 'bg-primary' : 'bg-warning'}`}>
          <div className="card-body">
            <h6 className="card-title">Net Balance</h6>
            <h3>${net.toFixed(2)}</h3>
          </div>
        </div>
      </div>
    </div>
  )
}

function SpendingPieChart({ data }) {
  if (!data || data.length === 0) return <p>No expense data yet.</p>

  const chartData = data.map(d => ({
    name: d.category,
    value: parseFloat(d.total)
  }))

  return (
    <div className="card p-3 mb-4">
      <h5>Spending by Category</h5>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          >
            {chartData.map((_, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}

function MonthlyBarChart({ data }) {
  if (!data || data.length === 0) return <p>No monthly data yet.</p>

  return (
    <div className="card p-3 mb-4">
      <h5>Monthly Income vs Expenses</h5>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
          <Legend />
          <Bar dataKey="income" fill="#22c55e" name="Income" />
          <Bar dataKey="expense" fill="#ef4444" name="Expenses" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default function TransactionsApp() {
  const [transactions, setTransactions] = useState([])
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(EMPTY_FORM)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)

  function fetchData() {
    Promise.all([
      fetch('/finance/api/transactions/').then(r => r.json()),
      fetch('/finance/api/summary/').then(r => r.json()),
    ]).then(([txData, summaryData]) => {
      setTransactions(txData)
      setSummary(summaryData)
      setLoading(false)
    })
  }

  useEffect(() => { fetchData() }, [])

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  function handleSubmit(e) {
    e.preventDefault()
    setSubmitting(true)
    setError(null)

    fetch('/finance/api/transactions/add/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify(form),
    })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'ok') {
          setForm(EMPTY_FORM)
          setShowForm(false)
          fetchData() // re-fetch everything so charts update too
        } else {
          setError('Something went wrong. Please try again.')
        }
        setSubmitting(false)
      })
  }

  if (loading) return <p>Loading...</p>

  return (
    <div>
      {/* Summary Cards */}
      {summary && (
        <SummaryCards
          income={summary.total_income}
          expenses={summary.total_expenses}
          net={summary.net}
        />
      )}

      {/* Charts */}
      <div className="row">
        <div className="col-md-6">
          {summary && <SpendingPieChart data={summary.by_category} />}
        </div>
        <div className="col-md-6">
          {summary && <MonthlyBarChart data={summary.monthly} />}
        </div>
      </div>

      {/* Add Transaction Button */}
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Transactions</h2>
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : '+ Add Transaction'}
        </button>
      </div>

      {/* Form */}
      {showForm && (
        <form onSubmit={handleSubmit} className="card p-4 mb-4">
          <h5 className="mb-3">New Transaction</h5>
          {error && <div className="alert alert-danger">{error}</div>}
          <div className="row g-3">
            <div className="col-md-3">
              <label className="form-label">Date</label>
              <input type="date" name="date" className="form-control"
                value={form.date} onChange={handleChange} required />
            </div>
            <div className="col-md-2">
              <label className="form-label">Amount</label>
              <input type="number" name="amount" step="0.01" className="form-control"
                value={form.amount} onChange={handleChange} required />
            </div>
            <div className="col-md-3">
              <label className="form-label">Category</label>
              <input type="text" name="category" className="form-control"
                value={form.category} onChange={handleChange} required />
            </div>
            <div className="col-md-2">
              <label className="form-label">Type</label>
              <select name="type" className="form-select"
                value={form.type} onChange={handleChange}>
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
            </div>
            <div className="col-md-2">
              <label className="form-label">Description</label>
              <input type="text" name="description" className="form-control"
                value={form.description} onChange={handleChange} />
            </div>
          </div>
          <button type="submit" className="btn btn-success mt-3" disabled={submitting}>
            {submitting ? 'Saving...' : 'Save Transaction'}
          </button>
        </form>
      )}

      {/* Table */}
      {transactions.length === 0 ? (
        <p>No transactions yet.</p>
      ) : (
        <table className="table table-hover table-bordered">
          <thead className="table-dark">
            <tr>
              <th>Date</th>
              <th>Category</th>
              <th>Description</th>
              <th>Amount</th>
              <th>Type</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((t, i) => (
              <tr key={i} className={t.type === 'expense' ? 'table-danger' : 'table-success'}>
                <td>{t.date}</td>
                <td>{t.category}</td>
                <td>{t.description || '—'}</td>
                <td>${parseFloat(t.amount).toFixed(2)}</td>
                <td>{t.type}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}