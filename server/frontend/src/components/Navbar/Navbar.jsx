import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function Navbar() {
  const [user, setUser] = useState(null)

  useEffect(() => {
    const username = localStorage.getItem('username')
    if (username) {
      setUser(username)
    }
  }, [])

  const logout = () => {
    localStorage.removeItem('username')
    localStorage.removeItem('user')
    window.location.href = '/'
  }

  return (
    <nav style={{ padding: '1rem', backgroundColor: '#333', color: 'white', display: 'flex', gap: '1rem', alignItems: 'center' }}>
      <Link to='/' style={{ color: 'white', textDecoration: 'none' }}>Home</Link>
      <Link to='/dealers' style={{ color: 'white', textDecoration: 'none' }}>Dealers</Link>
      <Link to='/about' style={{ color: 'white', textDecoration: 'none' }}>About Us</Link>
      <Link to='/contact' style={{ color: 'white', textDecoration: 'none' }}>Contact Us</Link>
      {!user ? (
        <>
          <Link to='/login' style={{ color: 'white', textDecoration: 'none' }}>Login</Link>
          <Link to='/register' style={{ color: 'white', textDecoration: 'none' }}>Register</Link>
        </>
      ) : (
        <>
          <span>Logged-in: {user}</span>
          <button onClick={logout} style={{ background: 'none', color: 'white', border: '1px solid white', padding: '0.25rem 0.5rem', cursor: 'pointer' }}>Logout</button>
        </>
      )}
    </nav>
  )
}

export default Navbar
