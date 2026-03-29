import React from 'react'
import './MessageItem.css'

/**
 * 单条消息组件
 */
export default function MessageItem({ message }) {
  const { role, content, timestamp } = message
  const isUser = role === 'user'

  return (
    <div className={`message ${isUser ? 'user-message' : 'agent-message'}`}>
      <div className="message-avatar">
        {isUser ? '👤' : '🤖'}
      </div>
      <div className="message-content">
        <div className="message-text">{content}</div>
        {timestamp && (
          <div className="message-time">
            {new Date(timestamp).toLocaleTimeString()}
          </div>
        )}
      </div>
    </div>
  )
}
