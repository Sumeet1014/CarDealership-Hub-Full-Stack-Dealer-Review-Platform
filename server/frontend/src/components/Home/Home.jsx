import React from 'react'
import { Link } from 'react-router-dom'

function Home() {
  return (
    <div style={{ padding: '2rem' }}>
      <h1>Cars Dealership</h1>
      <p>Welcome to our dealership network</p>
      <Link to='/dealers'>View Dealerships</Link>
    </div>
  )
}

export default Home
