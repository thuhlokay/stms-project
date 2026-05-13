import { useEffect, useState } from 'react'

import API_URL from '../services/api'


function Tutors() {

  const [tutors, setTutors] = useState([])

  const [message, setMessage] = useState('')


  useEffect(() => {

    fetch(`${API_URL}/tutors`)
      .then((response) => response.json())
      .then((data) => setTutors(data))

  }, [])


  const handleBooking = async (
    tutor_id: number
  ) => {

    try {

      const response = await fetch(
        `${API_URL}/book`,
        {
          method: 'POST',

          headers: {
            'Content-Type': 'application/json'
          },

          body: JSON.stringify({
            tutor_id: tutor_id,
            student_id: 1
          })
        }
      )

      const data = await response.json()

      setMessage(data.message)

    } catch (error) {

      setMessage('Booking failed')
    }
  }


  return (

    <div className="tutors-page">

      <h1>Available Tutors</h1>

      <p>{message}</p>

      <div className="tutor-grid">

        {tutors.map((tutor: any) => (

          <div
            key={tutor.profile_id}
            className="tutor-card"
          >

            <h2>{tutor.full_name}</h2>

            <p>
              {tutor.specialisation}
            </p>

            <button
              onClick={() =>
                handleBooking(tutor.profile_id)
              }
            >
              Book Session
            </button>

          </div>
        ))}

      </div>

    </div>
  )
}

export default Tutors