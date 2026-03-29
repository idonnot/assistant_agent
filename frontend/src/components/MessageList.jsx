import React from 'react'
import MessageItem from './MessageItem'
import './MessageList.css'

/**
 * 消息列表组件
 */
export default function MessageList({ messages, isLoading }) {
  const messagesEndRef = React.useRef(null)

  // 自动滚动到最新消息
  React.useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className="message-list">
      {messages.length === 0 ? (
        <div className="empty-state">
          <p>🤖 欢迎使用天气智能助手</p>
          <p>输入位置名称或直接问天气情况</p>
        </div>
      ) : (
        messages.map((message, index) => (
          <MessageItem key={index} message={message} />
        ))
      )}
      
      {isLoading && (
        <div className="loading-message">
          <div className="spinner"></div>
          <span>正在查询...</span>
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  )
}
