import { useState } from 'react'
import API_URL from '../services/api'

function Register() {

  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
    student_number: '',
    year_level: '',
    campus: '',
    phone_number: ''
  })

  const [message, setMessage] = useState('')


  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {

    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }


  const handleSubmit = async (
    e: React.SubmitEvent
  ) => {

    e.preventDefault()

    try {

      const response = await fetch(
        `${API_URL}/register`,
        {
          method: 'POST',

          headers: {
            'Content-Type': 'application/json'
          },

          body: JSON.stringify(formData)
        }
      )

      const data = await response.json()

      setMessage(data.message)

    } catch (error) {

      setMessage('Registration failed')
    }
  }


  return (
    <div className="register-container">

      <form
        className="register-form"
        onSubmit={handleSubmit}
      >

        <h2>Student Registration</h2>

        <input
          type="text"
          name="full_name"
          placeholder="Full Name"
          onChange={handleChange}
          required
        />

        <input
          type="email"
          name="email"
          placeholder="Email"
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={handleChange}
          required
        />

        <input
          type="text"
          name="student_number"
          placeholder="Student Number"
          onChange={handleChange}
        />


        <input
          type="number"
          name="year_level"
          placeholder="Year Level"
          onChange={handleChange}
        />

        <input
          type="text"
          name="campus"
          placeholder="Campus"
          onChange={handleChange}
        />

        <input
          type="text"
          name="phone_number"
          placeholder="Phone Number"
          onChange={handleChange}
        />

        <button type="submit">
          Register
        </button>

        <p>{message}</p>

      </form>
    </div>
  )
}

export default Register