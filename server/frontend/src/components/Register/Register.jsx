import React, { useState } from 'react'
import axios from 'axios'

function Register() {
  const [form, setForm] = useState({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    password: ''
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    if (!form.username || !form.first_name || !form.last_name || !form.email || !form.password) {
      setError('All fields are required')
      return
    }
    try {
      const res = await axios.post('http://localhost:8000/api/register/', form)
      setMessage(res.data.message || 'Registration successful')
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed')
    }
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '400px' }}>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <input name='username' placeholder='Username' value={form.username} onChange={handleChange} style={{ width: '100%', marginBottom: '0.5rem', padding: '0.5rem' }} />
        </div>
        <div>
          <input name='first_name' placeholder='First Name' value={form.first_name} onChange={handleChange} style={{ width: '100%', marginBottom: '0.5rem', padding: '0.5rem' }} />
        </div>
        <div>
          <input name='last_name' placeholder='Last Name' value={form.last_name} onChange={handleChange} style={{ width: '100%', marginBottom: '0.5rem', padding: '0.5rem' }} />
        </div>
        <div>
          <input name='email' type='email' placeholder='Email' value={form.email} onChange={handleChange} style={{ width: '100%', marginBottom: '0.5rem', padding: '0.5rem' }} />
        </div>
        <div>
          <input name='password' type='password' placeholder='Password' value={form.password} onChange={handleChange} style={{ width: '100%', marginBottom: '0.5rem', padding: '0.5rem' }} />
        </div>
        <button type='submit' style={{ padding: '0.5rem 1rem' }}>Register</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {message && <p style={{ color: 'green' }}>{message}</p>}
    </div>
  )
}

export default Register
