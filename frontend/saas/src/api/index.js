import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1/housekeeping',
  timeout: 30000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (res) => res.data,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api

export const getDashboard = () => api.get('/dashboard/overview')
export const getLeads = (params) => api.get('/leads/list', { params })
export const createLead = (data) => api.post('/leads/create', data)
export const scoreLead = (id) => api.post(`/leads/${id}/score`)
export const dispatchLead = (id) => api.post(`/leads/${id}/dispatch`)
export const generateContent = (data) => api.post('/contents/generate', data)
export const getCompanies = (params) => api.get('/companies/list', { params })
export const createCompany = (data) => api.post('/companies/create', data)
