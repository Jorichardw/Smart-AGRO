import { useState, useEffect } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import Layout from '@/components/layout/Layout'
import { api } from '@/lib/api'

export default function DashboardPage() {
  const [stats, setStats] = useState({
    totalFarms: 0,
    totalCrops: 0,
    activeDevices: 0,
    alerts: 0
  })
  const [weather, setWeather] = useState(null)
  const [recentActivities, setRecentActivities] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      // Fetch dashboard stats
      // const statsData = await api.get('/analytics/stats')
      // setStats(statsData.data)

      // Fetch weather
      const weatherData = await api.get('/weather/current', {
        params: { lat: 28.6139, lon: 77.2090 }
      })
      setWeather(weatherData.data)

      // Mock data for demo
      setStats({
        totalFarms: 3,
        totalCrops: 12,
        activeDevices: 8,
        alerts: 2
      })

      setRecentActivities([
        { id: 1, type: 'disease', message: 'Disease detected in Tomato Crop', time: '2 hours ago', severity: 'high' },
        { id: 2, type: 'iot', message: 'Soil moisture low in Farm A', time: '4 hours ago', severity: 'medium' },
        { id: 3, type: 'weather', message: 'Heavy rain expected tomorrow', time: '6 hours ago', severity: 'low' },
      ])
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const quickActions = [
    { icon: '🦠', title: 'Disease Detection', href: '/disease-detection', color: 'bg-red-50 text-red-600' },
    { icon: '🐛', title: 'Pest Detection', href: '/pest-detection', color: 'bg-orange-50 text-orange-600' },
    { icon: '🌡️', title: 'Weather', href: '/weather', color: 'bg-blue-50 text-blue-600' },
    { icon: '📊', title: 'IoT Dashboard', href: '/iot', color: 'bg-purple-50 text-purple-600' },
    { icon: '🛒', title: 'Marketplace', href: '/marketplace', color: 'bg-green-50 text-green-600' },
    { icon: '🤖', title: 'AI Assistant', href: '/ai-assistant', color: 'bg-indigo-50 text-indigo-600' },
  ]

  return (
    <Layout>
      <Head>
        <title>Dashboard - AGRO-BOT</title>
      </Head>

      <div className="p-6">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome back! Here's your farm overview</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Farms</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">{stats.totalFarms}</p>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-2xl">
                🌾
              </div>
            </div>
            <div className="mt-4 flex items-center text-sm text-green-600">
              <span>↑ 12%</span>
              <span className="text-gray-500 ml-2">from last month</span>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Active Crops</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">{stats.totalCrops}</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-2xl">
                🌱
              </div>
            </div>
            <div className="mt-4 flex items-center text-sm text-blue-600">
              <span>↑ 8%</span>
              <span className="text-gray-500 ml-2">from last month</span>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">IoT Devices</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">{stats.activeDevices}</p>
              </div>
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center text-2xl">
                📡
              </div>
            </div>
            <div className="mt-4 flex items-center text-sm text-green-600">
              <span>All online</span>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Active Alerts</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">{stats.alerts}</p>
              </div>
              <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center text-2xl">
                🚨
              </div>
            </div>
            <div className="mt-4 flex items-center text-sm text-red-600">
              <span>Requires attention</span>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {quickActions.map((action, index) => (
              <Link
                key={index}
                href={action.href}
                className={`${action.color} rounded-xl p-4 text-center hover:shadow-md transition-shadow`}
              >
                <div className="text-3xl mb-2">{action.icon}</div>
                <p className="text-sm font-medium">{action.title}</p>
              </Link>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Weather Widget */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Current Weather</h3>
            {weather ? (
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="text-5xl">☀️</div>
                  <div className="text-right">
                    <p className="text-4xl font-bold">{Math.round(weather.main?.temp || 25)}°C</p>
                    <p className="text-gray-600">{weather.weather?.[0]?.description || 'Clear sky'}</p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="flex items-center">
                    <span className="mr-2">💧</span>
                    <span>Humidity: {weather.main?.humidity || 65}%</span>
                  </div>
                  <div className="flex items-center">
                    <span className="mr-2">🌬️</span>
                    <span>Wind: {Math.round(weather.wind?.speed || 10)} km/h</span>
                  </div>
                </div>
                <Link href="/weather" className="block mt-4 text-center text-blue-600 hover:text-blue-700 font-medium">
                  View Forecast →
                </Link>
              </div>
            ) : (
              <p className="text-gray-500">Loading weather data...</p>
            )}
          </div>

          {/* Recent Activities */}
          <div className="lg:col-span-2 bg-white rounded-xl shadow-sm p-6 border border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Recent Activities</h3>
              <Link href="/notifications" className="text-sm text-blue-600 hover:text-blue-700">
                View all
              </Link>
            </div>
            <div className="space-y-3">
              {recentActivities.map((activity) => (
                <div key={activity.id} className="flex items-start p-3 bg-gray-50 rounded-lg">
                  <div className={`w-2 h-2 rounded-full mt-2 mr-3 ${
                    activity.severity === 'high' ? 'bg-red-500' :
                    activity.severity === 'medium' ? 'bg-yellow-500' :
                    'bg-blue-500'
                  }`}></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{activity.message}</p>
                    <p className="text-xs text-gray-500 mt-1">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}
