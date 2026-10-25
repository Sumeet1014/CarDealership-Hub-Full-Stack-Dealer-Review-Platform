import apiUrl from '../../api'
import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'

function Dealer() {
  const { id } = useParams()
  const [dealer, setDealer] = useState(null)
  const [reviews, setReviews] = useState([])

  useEffect(() => {
    axios.get(apiUrl('/api/dealers/' + id + '/'))
      .then(res => setDealer(res.data))
      .catch(err => console.error(err))
    axios.get(apiUrl('/api/dealers/' + id + '/reviews/'))
      .then(res => setReviews(res.data))
      .catch(err => console.error(err))
  }, [id])

  if (!dealer) return <div style={{ padding: '2rem' }}>Loading...</div>

  return (
    <div style={{ padding: '2rem' }}>
      <h2>{dealer.name}</h2>
      {dealer.image && <img src={dealer.image} alt={dealer.name} style={{ width: '300px', height: '200px', objectFit: 'cover' }} />}
      <p><strong>Address:</strong> {dealer.address}</p>
      <p><strong>City:</strong> {dealer.city}</p>
      <p><strong>State:</strong> {dealer.state}</p>
      <p><strong>ZIP:</strong> {dealer.zip}</p>
      <p><strong>Phone:</strong> {dealer.phone}</p>
      <p><strong>Website:</strong> {dealer.website}</p>
      <p><strong>Description:</strong> {dealer.description}</p>
      <h3>Reviews</h3>
      {reviews.map(review => (
        <div key={review.id} style={{ border: '1px solid #ddd', padding: '1rem', marginBottom: '0.5rem', backgroundColor: 'white' }}>
          <p><strong>{review.user}</strong> - Rating: {review.rating}/5</p>
          <p>{review.review_text}</p>
          {review.sentiment && <p><em>Sentiment: {review.sentiment}</em></p>}
        </div>
      ))}
    </div>
  )
}

export default Dealer
