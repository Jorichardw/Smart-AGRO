import React, { useEffect, useState } from 'react'
import Head from 'next/head'
import { useRouter } from 'next/router'
import Header from './Header'
import Sidebar from './Sidebar'
import apiClient from '@/lib/api'

const Layout = ({ children, title = 'AGRO-BOT & AUTOMATION', requireAuth = true }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const router = useRouter()

  useEffect(() => {
    if (requireAuth) {
      checkAuth()
    } else {
      setLoading(false)
    }
  }, [requireAuth])

  const checkAuth = async () => {
    try {
      const token = apiClient.getAuthToken()
      if (!token) {
        router.push('/')
        return
      }

      const userData = await apiClient.getCurrentUser()
      setUser(userData)
    } catch (error) {
      console.error('Auth check failed:', error)
      apiClient.setAuthToken(null)
      router.push('/')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    try {
      await apiClient.logout()
      setUser(null)
      router.push('/')
    } catch (error) {
      console.error('Logout failed:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>
    )
  }

  // Public layout (no auth required)
  if (!requireAuth) {
    return (
      <>
        <Head>
          <title>{title}</title>
          <meta name="description" content="AI-Powered Smart Agriculture Platform" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <div className="min-h-screen bg-gray-50">
          {children}
        </div>
      </>
    )
  }

  // Authenticated layout
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="description" content="AI-Powered Smart Agriculture Platform" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <Header user={user} onLogout={handleLogout} />
        
        <div className="flex">
          {/* Sidebar */}
          <Sidebar 
            isOpen={sidebarOpen} 
            onClose={() => setSidebarOpen(false)} 
            user={user}
          />
          
          {/* Main Content */}
          <main className="flex-1 lg:pl-64">
            <div className="py-6">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {children}
              </div>
            </div>
          </main>
        </div>
        
        {/* Mobile sidebar backdrop */}
        {sidebarOpen && (
          <div 
            className="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}
      </div>
    </>
  )
}

export default Layout