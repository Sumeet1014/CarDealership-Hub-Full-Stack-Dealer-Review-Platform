import apiUrl from '../../api'
import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

function Dealers() {
  const [dealers, setDealers] = useState([])
  const [user, setUser] = useState(null)

  useEffect(() => {
    const username = localStorage.getItem('username')
    setUser(username)
    axios.get(apiUrl('/api/dealers/'))
      .then(res => {
        if (Array.isArray(res.data)) {
          setDealers(res.data)
        } else {
          setDealers([])
        }
      })
      .catch(err => {
        console.error(err)
        setDealers([])
      })
  }, [])

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Dealers</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem' }}>
        {dealers.map(dealer => (
          <div key={dealer.id} style={{ border: '1px solid #ddd', padding: '1rem', borderRadius: '8px', backgroundColor: 'white' }}>
            {dealer.image && <img src={dealer.image} alt={dealer.name} style={{ width: '100%', height: '200px', objectFit: 'cover' }} />}
            <h3>{dealer.name}</h3>
            <p>{dealer.city}, {dealer.state}</p>
            <p>{dealer.address}</p>
            <p>{dealer.phone}</p>
            <Link to={"/dealer/" + dealer.id}>View Details</Link>
            {user && <><br /><Link to={"/dealer/" + dealer.id + "/review"}>Review Dealer</Link></>}
          </div>
        ))}
      </div>
    </div>
  )
}

export default Dealers
