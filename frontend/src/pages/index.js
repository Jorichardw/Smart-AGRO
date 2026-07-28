import Head from 'next/head'
import { useState, useEffect } from 'react'
import Layout from '@/components/layout/Layout'

export default function Home() {
  const [apiStatus, setApiStatus] = useState('checking...')

  useEffect(() => {
    // Check API health
    fetch('http://localhost:8000/health')
      .then(res => res.json())
      .then(data => {
        if (data.status === 'healthy') {
          setApiStatus('connected ✅')
        } else {
          setApiStatus('unhealthy ⚠️')
        }
      })
      .catch(() => {
        setApiStatus('disconnected ❌')
      })
  }, [])

  return (
    <Layout requireAuth={false} title="AGRO-BOT & AUTOMATION - Smart Agriculture Platform">
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
        <main className="container mx-auto px-4 py-16">
          <div className="text-center">
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              🌾 AGRO-BOT & AUTOMATION
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              AI-Powered Smart Agriculture Platform for modern farming
            </p>
            
            <div className="bg-white rounded-xl shadow-lg p-8 max-w-4xl mx-auto">
              <h2 className="text-2xl font-semibold mb-6">Platform Status</h2>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-green-50 p-6 rounded-lg">
                  <h3 className="text-lg font-medium text-green-800 mb-2">
                    🖥️ Frontend
                  </h3>
                  <p className="text-green-600">
                    React App: <span className="font-semibold">Running ✅</span>
                  </p>
                </div>
                
                <div className="bg-blue-50 p-6 rounded-lg">
                  <h3 className="text-lg font-medium text-blue-800 mb-2">
                    🔗 Backend API
                  </h3>
                  <p className="text-blue-600">
                    Status: <span className="font-semibold">{apiStatus}</span>
                  </p>
                </div>
              </div>

              <div className="mt-8 grid md:grid-cols-3 gap-4">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-medium mb-2">🌱 Crop Management</h4>
                  <p className="text-sm text-gray-600">Complete farm lifecycle tracking</p>
                </div>
                
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-medium mb-2">🦠 Disease Detection</h4>
                  <p className="text-sm text-gray-600">AI-powered plant health analysis</p>
                </div>
                
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-medium mb-2">💧 Smart Irrigation</h4>
                  <p className="text-sm text-gray-600">IoT-based water management</p>
                </div>
                
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-medium mb-2">🌡️ Weather Monitoring</h4>
                  <p className="text-sm text-gray-600">Real-time weather data & alerts</p>
                </div>
                
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-medium mb-2">🛒 Marketplace</h4>
                  <p className="text-sm text-gray-600">Agricultural e-commerce platform</p>
                </div>
                
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h4 className="font-medium mb-2">🤖 AI Assistant</h4>
                  <p className="text-sm text-gray-600">Voice-enabled farming advisor</p>
                </div>
              </div>

              <div className="mt-8 text-center">
                <div className="inline-flex space-x-4">
                  <button 
                    onClick={() => window.open('http://localhost:8000/docs', '_blank')}
                    className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors"
                  >
                    📖 API Documentation
                  </button>
                  
                  <button 
                    onClick={() => window.location.href = '/login'}
                    className="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-lg transition-colors"
                  >
                    🔐 Login
                  </button>
                  
                  <button 
                    onClick={() => window.location.href = '/dashboard'}
                    className="bg-purple-500 hover:bg-purple-600 text-white px-6 py-2 rounded-lg transition-colors"
                  >
                    📊 Dashboard
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
        
        <footer className="text-center py-8 text-gray-500">
          <p>© 2024 AGRO-BOT & AUTOMATION. Built for Smart India Hackathon 2025.</p>
        </footer>
      </div>
    </Layout>
  )
}