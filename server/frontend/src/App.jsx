import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './components/Home/Home'
import Login from './components/Login/Login'
import Register from './components/Register/Register'
import Dealers from './components/Dealers/Dealers'
import Dealer from './components/Dealers/Dealer'
import DealerReview from './components/Dealers/DealerReview'
import About from './components/About/About'
import Contact from './components/Contact/Contact'
import Navbar from './components/Navbar/Navbar'

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/login' element={<Login />} />
        <Route path='/register' element={<Register />} />
        <Route path='/dealers' element={<Dealers />} />
        <Route path='/dealer/:id' element={<Dealer />} />
        <Route path='/dealer/:id/review' element={<DealerReview />} />
        <Route path='/about' element={<About />} />
        <Route path='/contact' element={<Contact />} />
      </Routes>
    </Router>
  )
}

export default App
