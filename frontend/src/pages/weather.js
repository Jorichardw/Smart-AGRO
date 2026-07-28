import { useState, useEffect } from 'react'
import Head from 'next/head'
import Layout from '@/components/layout/Layout'
import { api } from '@/lib/api'

export default function WeatherPage() {
  const [weather, setWeather] = useState(null)
  const [forecast, setForecast] = useState([])
  const [location, setLocation] = useState({ lat: 28.6139, lon: 77.2090 })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchWeatherData()
  }, [])

  const fetchWeatherData = async () => {
    try {
      // Fetch current weather
      const currentWeather = await api.get('/weather/current', {
        params: location
      })
      setWeather(currentWeather.data)

      // Fetch forecast
      const forecastData = await api.get('/weather/forecast', {
        params: { ...location, days: 7 }
      })
      setForecast(forecastData.data.forecast || [])
    } catch (error) {
      console.error('Error fetching weather:', error)
    } finally {
      setLoading(false)
    }
  }

  const getWeatherIcon = (condition) => {
    const icons = {
      'clear': '☀️',
      'clouds': '☁️',
      'rain': '🌧️',
      'snow': '❄️',
      'thunderstorm': '⛈️',
      'drizzle': '🌦️',
      'mist': '🌫️'
    }
    return icons[condition?.toLowerCase()] || '🌤️'
  }

  return (
    <Layout>
      <Head>
        <title>Weather - AGRO-BOT</title>
      </Head>

      <div className="p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Weather Monitoring</h1>

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading weather data...</p>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Current Weather Card */}
            <div className="bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl p-8 text-white shadow-xl">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-semibold mb-2">Current Weather</h2>
                  <p className="text-blue-100">Delhi, India</p>
                </div>
                <div className="text-7xl">
                  {getWeatherIcon(weather?.weather?.[0]?.main)}
                </div>
              </div>
              
              <div className="mt-8 flex items-end">
                <div className="text-6xl font-bold">{Math.round(weather?.main?.temp || 25)}°</div>
                <div className="ml-4 mb-2">
                  <p className="text-xl capitalize">{weather?.weather?.[0]?.description || 'Clear sky'}</p>
                  <p className="text-blue-100">Feels like {Math.round(weather?.main?.feels_like || 24)}°</p>
                </div>
              </div>

              <div className="mt-8 grid grid-cols-4 gap-4">
                <div>
                  <p className="text-blue-100 text-sm">Humidity</p>
                  <p className="text-2xl font-semibold">{weather?.main?.humidity || 65}%</p>
                </div>
                <div>
                  <p className="text-blue-100 text-sm">Wind Speed</p>
                  <p className="text-2xl font-semibold">{Math.round(weather?.wind?.speed || 10)} km/h</p>
                </div>
                <div>
                  <p className="text-blue-100 text-sm">Pressure</p>
                  <p className="text-2xl font-semibold">{weather?.main?.pressure || 1013} hPa</p>
                </div>
                <div>
                  <p className="text-blue-100 text-sm">Visibility</p>
                  <p className="text-2xl font-semibold">{Math.round((weather?.visibility || 10000) / 1000)} km</p>
                </div>
              </div>
            </div>

            {/* 7-Day Forecast */}
            <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">7-Day Forecast</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
                {[...Array(7)].map((_, index) => {
                  const date = new Date()
                  date.setDate(date.getDate() + index)
                  return (
                    <div key={index} className="text-center p-4 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors">
                      <p className="text-sm font-medium text-gray-600">
                        {index === 0 ? 'Today' : date.toLocaleDateString('en-US', { weekday: 'short' })}
                      </p>
                      <div className="text-4xl my-3">{getWeatherIcon('clear')}</div>
                      <div className="text-sm">
                        <span className="font-semibold">{25 + Math.floor(Math.random() * 10)}°</span>
                        <span className="text-gray-500 ml-1">{15 + Math.floor(Math.random() * 5)}°</span>
                      </div>
                      <p className="text-xs text-gray-500 mt-2">☔ {Math.floor(Math.random() * 30)}%</p>
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Weather Alerts */}
            <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Weather Alerts</h3>
              <div className="space-y-3">
                <div className="flex items-start p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <span className="text-2xl mr-3">⚠️</span>
                  <div>
                    <p className="font-semibold text-gray-900">Heavy Rain Warning</p>
                    <p className="text-sm text-gray-600 mt-1">Heavy rainfall expected tomorrow afternoon. Take necessary precautions.</p>
                    <p className="text-xs text-gray-500 mt-2">Valid until: Tomorrow 6:00 PM</p>
                  </div>
                </div>
                <div className="flex items-start p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <span className="text-2xl mr-3">ℹ️</span>
                  <div>
                    <p className="font-semibold text-gray-900">Temperature Drop</p>
                    <p className="text-sm text-gray-600 mt-1">Temperatures will drop by 5°C in the next 48 hours.</p>
                    <p className="text-xs text-gray-500 mt-2">Valid for: Next 2 days</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  )
}
