import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'

function DealerReview() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [reviewText, setReviewText] = useState('')
  const [rating, setRating] = useState(5)
  const [user, setUser] = useState(null)
  const [message, setMessage] = useState('')

  useEffect(() => {
    const username = localStorage.getItem('username')
    if (!username) {
      navigate('/login')
      return
    }
    setUser(username)
  }, [navigate])

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await axios.post(http://localhost:8000/api/dealers//reviews/, {
        review_text: reviewText,
        rating: rating,
        user: user
      })
      setMessage('Review submitted')
      setTimeout(() => navigate(/dealer/), 1000)
    } catch (err) {
      setMessage('Error submitting review')
    }
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '500px' }}>
      <h2>Submit Review</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <textarea placeholder='Review text' value={reviewText} onChange={(e) => setReviewText(e.target.value)} style={{ width: '100%', height: '100px', marginBottom: '0.5rem', padding: '0.5rem' }} required />
        </div>
        <div>
          <select value={rating} onChange={(e) => setRating(e.target.value)} style={{ marginBottom: '0.5rem', padding: '0.5rem' }}>
            <option value={5}>5</option>
            <option value={4}>4</option>
            <option value={3}>3</option>
            <option value={2}>2</option>
            <option value={1}>1</option>
          </select>
        </div>
        <button type='submit' style={{ padding: '0.5rem 1rem' }}>Submit</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  )
}

export default DealerReview
