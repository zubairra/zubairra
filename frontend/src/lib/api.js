import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'
})

export const getDailyPerformance = async (memberId) => {
  const { data } = await api.get('/performance/daily', { params: { member_id: memberId } })
  return data
}

export const getMonthlyPnl = async (memberId, aggregate = false) => {
  const { data } = await api.get('/performance/monthly', { params: { member_id: memberId, aggregate } })
  return data
}

export const updateToken = async (memberId, payload) => {
  const { data } = await api.patch(`/users/${memberId}/token`, payload)
  return data
}

export const runSync = async (memberId) => {
  const { data } = await api.post('/sync/daily', { member_id: memberId })
  return data
}
