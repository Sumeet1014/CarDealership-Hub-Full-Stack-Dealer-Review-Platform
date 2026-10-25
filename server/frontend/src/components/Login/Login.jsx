import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

function Login() {
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const res = await axios.post('http://localhost:8000/api/login/', form)
      if (res.data.user) {
        localStorage.setItem('username', res.data.user.username)
        localStorage.setItem('user', JSON.stringify(res.data.user))
        window.location.href = '/'
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed')
    }
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '400px' }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <input name='username' placeholder='Username' value={form.username} onChange={handleChange} style={{ width: '100%', marginBottom: '0.5rem', padding: '0.5rem' }} />
        </div>
        <div>
          <input name='password' type='password' placeholder='Password' value={form.password} onChange={handleChange} style={{ width: '100%', marginBottom: '0.5rem', padding: '0.5rem' }} />
        </div>
        <button type='submit' style={{ padding: '0.5rem 1rem' }}>Login</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  )
}

export default Login
