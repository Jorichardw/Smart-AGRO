import { apiUrl } from './utils'

class APIClient {
  constructor() {
    this.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    this.token = null
  }

  setAuthToken(token) {
    this.token = token
    if (typeof window !== 'undefined') {
      if (token) {
        localStorage.setItem('auth_token', token)
      } else {
        localStorage.removeItem('auth_token')
      }
    }
  }

  getAuthToken() {
    if (this.token) return this.token
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token')
    }
    return null
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const token = this.getAuthToken()
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    }

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || errorData.message || `HTTP ${response.status}`)
      }

      const contentType = response.headers.get('content-type')
      if (contentType && contentType.includes('application/json')) {
        return await response.json()
      }
      
      return response
    } catch (error) {
      console.error('API Request Error:', error)
      throw error
    }
  }

  async get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString()
    const url = queryString ? `${endpoint}?${queryString}` : endpoint
    return this.request(url)
  }

  async post(endpoint, data = {}, isFormData = false) {
    const options = {
      method: 'POST',
      body: isFormData ? data : JSON.stringify(data)
    }
    
    if (isFormData) {
      // Remove Content-Type header for FormData
      options.headers = {}
      const token = this.getAuthToken()
      if (token) {
        options.headers.Authorization = `Bearer ${token}`
      }
    }
    
    return this.request(endpoint, options)
  }

  async put(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  async patch(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'PATCH', 
      body: JSON.stringify(data)
    })
  }

  async delete(endpoint) {
    return this.request(endpoint, {
      method: 'DELETE'
    })
  }

  // Authentication methods
  async login(firebaseToken) {
    const response = await this.post('/api/v1/auth/login', {
      firebase_id_token: firebaseToken
    })
    
    if (response.access_token) {
      this.setAuthToken(response.access_token)
    }
    
    return response
  }

  async register(userData) {
    const response = await this.post('/api/v1/auth/register', userData)
    
    if (response.access_token) {
      this.setAuthToken(response.access_token)
    }
    
    return response
  }

  async logout() {
    try {
      await this.post('/api/v1/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      this.setAuthToken(null)
    }
  }

  async getCurrentUser() {
    return this.get('/api/v1/users/me')
  }

  // Farm management
  async getFarms() {
    return this.get('/api/v1/farms/')
  }

  async createFarm(farmData) {
    return this.post('/api/v1/farms/', farmData)
  }

  async getFarm(farmId) {
    return this.get(`/api/v1/farms/${farmId}`)
  }

  async updateFarm(farmId, farmData) {
    return this.put(`/api/v1/farms/${farmId}`, farmData)
  }

  async deleteFarm(farmId) {
    return this.delete(`/api/v1/farms/${farmId}`)
  }

  async getFarmPlots(farmId) {
    return this.get(`/api/v1/farms/${farmId}/plots`)
  }

  async createPlot(farmId, plotData) {
    return this.post(`/api/v1/farms/${farmId}/plots`, plotData)
  }

  // Weather services
  async getCurrentWeather(latitude, longitude) {
    return this.get('/api/v1/weather/current', { latitude, longitude })
  }

  async getWeatherForecast(latitude, longitude, days = 7) {
    return this.get('/api/v1/weather/forecast', { latitude, longitude, days })
  }

  async getWeatherAlerts(latitude, longitude) {
    return this.get('/api/v1/weather/alerts', { latitude, longitude })
  }

  // AI services
  async detectDisease(imageFile, cropId = null) {
    const formData = new FormData()
    formData.append('image', imageFile)
    if (cropId) {
      formData.append('crop_id', cropId)
    }
    
    return this.post('/api/v1/ai/disease-detection', formData, true)
  }

  async detectPest(imageFile, cropId = null) {
    const formData = new FormData()
    formData.append('image', imageFile)
    if (cropId) {
      formData.append('crop_id', cropId)
    }
    
    return this.post('/api/v1/ai/pest-detection', formData, true)
  }

  async getCropRecommendations(soilData, latitude, longitude) {
    return this.post('/api/v1/ai/crop-recommendations', {
      soil_data: soilData,
      latitude,
      longitude
    })
  }

  async getPredictedYield(cropId) {
    return this.get(`/api/v1/ai/yield-prediction/${cropId}`)
  }

  async chatWithAI(message, context = null) {
    const formData = new FormData()
    formData.append('message', message)
    if (context) {
      formData.append('context', context)
    }
    
    return this.post('/api/v1/ai/chat', formData, true)
  }

  // Health check
  async getHealth() {
    return this.get('/health')
  }

  async getAPIInfo() {
    return this.get('/api/info')
  }
}

// Create and export a singleton instance
const apiClient = new APIClient()

export default apiClient
export { APIClient }