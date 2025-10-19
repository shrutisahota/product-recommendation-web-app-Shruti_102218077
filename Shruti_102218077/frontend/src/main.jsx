import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Recommend from './pages/Recommend.jsx'
import Analytics from './pages/Analytics.jsx'
import './index.css'

function Shell() {
  return (
    <div className="min-h-screen">
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="font-semibold text-lg">Shruti_102218077</div>
          <nav className="space-x-4">
            <Link className="text-gray-700 hover:text-black" to="/">Recommend</Link>
            <Link className="text-gray-700 hover:text-black" to="/analytics">Analytics</Link>
          </nav>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-4 py-6">
        <Routes>
          <Route path="/" element={<Recommend />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </main>
      <footer className="text-center text-sm text-gray-500 py-6">© 2025</footer>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <Shell />
  </BrowserRouter>
)
