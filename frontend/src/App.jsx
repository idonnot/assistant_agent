import React, { useState, useEffect } from 'react'
import './App.css'
import ChatBox from './components/ChatBox'
import MessageList from './components/MessageList'
import { sendChatMessage, checkHealth } from './services/api'

function App() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState('checking')
  const [threadId] = useState(`user_${Date.now()}`)

  // 检查后端连接
  useEffect(() => {
    const checkConnection = async () => {
      try {
        await checkHealth()
        setConnectionStatus('connected')
      } catch (error) {
        console.error('Backend connection failed:', error)
        setConnectionStatus('disconnected')
      }
    }

    checkConnection()
    const interval = setInterval(checkConnection, 30000) // 每30秒检查一次

    return () => clearInterval(interval)
  }, [])

  // 处理发送消息
  const handleSendMessage = async (text) => {
    // 添加用户消息到UI
    const userMessage = {
      role: 'user',
      content: text,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, userMessage])

    setIsLoading(true)
    try {
      // 调用API
      const response = await sendChatMessage(text, threadId)

      // 添加代理的响应
      const agentMessage = {
        role: 'agent',
        content: response.response,
        timestamp: new Date(),
        status: response.status
      }
      setMessages(prev => [...prev, agentMessage])

      if (response.status !== 'ok') {
        console.warn('Agent warning:', response.response)
      }
    } catch (error) {
      // 添加错误消息
      const errorMessage = {
        role: 'agent',
        content: `❌ 错误: ${error.message || '无法连接到服务器'}`,
        timestamp: new Date(),
        status: 'error'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌤️ 天气智能助手</h1>
        <div className="status-indicator">
          {connectionStatus === 'connected' && (
            <span className="status connected">✅ 已连接</span>
          )}
          {connectionStatus === 'disconnected' && (
            <span className="status disconnected">❌ 未连接</span>
          )}
          {connectionStatus === 'checking' && (
            <span className="status checking">⏳ 检查中</span>
          )}
        </div>
      </header>

      <main className="app-main">
        <MessageList messages={messages} isLoading={isLoading} />
      </main>

      <footer className="app-footer">
        <ChatBox
          onSendMessage={handleSendMessage}
          disabled={connectionStatus === 'disconnected'}
        />
        <p className="footer-hint">提示: 输入地名或问题，例如"杭州天气"、"北京今天天气怎么样"</p>
      </footer>
    </div>
  )
}

export default App
