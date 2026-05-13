import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import API_URL from '../services/api'

function Login() {

  const navigate = useNavigate()

  const [email, setEmail] = useState('')

  const [password, setPassword] = useState('')

  const [message, setMessage] = useState('')


  const handleSubmit = async (
    e: React.FormEvent
  ) => {

    e.preventDefault()

    try {

      const response = await fetch(
        `${API_URL}/login`,
        {
          method: 'POST',

          headers: {
            'Content-Type': 'application/json'
          },

          body: JSON.stringify({
            email,
            password
          })
        }
      )

      const data = await response.json()

      if (data.message === 'Login successful') {

        navigate('/dashboard')

      } else {

        setMessage(data.message)
      }

    } catch (error) {

      setMessage('Login failed')
    }
  }


  return (

    <div className="register-container">

      <form
        className="register-form"
        onSubmit={handleSubmit}
      >

        <h2>Login</h2>

        <input
          type="email"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">
          Login
        </button>

        <p>{message}</p>

      </form>

    </div>
  )
}

export default Login