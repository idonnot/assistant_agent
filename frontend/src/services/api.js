import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * 创建axios实例，用于与后端API通信
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * 发送单条聊天消息 (HTTP POST)
 * @param {string} message - 用户消息
 * @param {string} threadId - 会话ID
 * @returns {Promise} 响应数据
 */
export const sendChatMessage = async (message, threadId = 'default_user') => {
  try {
    const response = await apiClient.post('/api/chat', {
      message,
      thread_id: threadId
    })
    return response.data
  } catch (error) {
    console.error('Chat API error:', error)
    throw error
  }
}

/**
 * 创建WebSocket连接用于实时聊天
 * @param {string} threadId - 会话ID
 * @param {Function} onMessage - 接收消息的回调
 * @param {Function} onError - 错误处理回调
 * @returns {WebSocket} WebSocket连接实例
 */
export const createWebSocketConnection = (threadId = 'default_user', onMessage, onError) => {
  const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const wsUrl = `${wsProtocol}//${window.location.host}/api/ws?thread_id=${threadId}`
  
  const ws = new WebSocket(wsUrl)
  
  ws.onopen = () => {
    console.log('WebSocket connected')
  }
  
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      onMessage(data)
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error)
    }
  }
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
    if (onError) {
      onError(error)
    }
  }
  
  ws.onclose = () => {
    console.log('WebSocket disconnected')
  }
  
  return ws
}

/**
 * 检查后端健康状态
 * @returns {Promise} 响应数据
 */
export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/health')
    return response.data
  } catch (error) {
    console.error('Health check failed:', error)
    throw error
  }
}
