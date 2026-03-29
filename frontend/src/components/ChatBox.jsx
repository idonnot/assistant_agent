import React, { useState } from 'react'
import './ChatBox.css'

/**
 * 聊天输入框组件
 */
export default function ChatBox({ onSendMessage, disabled = false }) {
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!input.trim()) return
    
    setIsLoading(true)
    try {
      // 调用父组件的发送消息函数
      await onSendMessage(input)
      setInput('')  // 清空输入框
    } catch (error) {
      console.error('Failed to send message:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form className="chat-box" onSubmit={handleSubmit}>
      <div className="input-container">
        <input
          type="text"
          className="chat-input"
          placeholder="输入位置名称或问题... 例如：杭州的天气"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={disabled || isLoading}
          autoFocus
        />
        <button
          type="submit"
          className="send-button"
          disabled={disabled || isLoading || !input.trim()}
        >
          {isLoading ? '⏳ 发送中...' : '📤 发送'}
        </button>
      </div>
    </form>
  )
}
