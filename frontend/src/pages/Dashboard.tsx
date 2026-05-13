function Dashboard() {

  return (

    <div className="dashboard-page">

      <h1>
        Student Dashboard
      </h1>

      <div className="dashboard-grid">

        <div className="dashboard-card">
          <h2>Bookings</h2>
          <p>
            View upcoming tutor sessions.
          </p>
        </div>

        <div className="dashboard-card">
          <h2>Find Tutors</h2>
          <p>
            Browse available tutors.
          </p>
        </div>

        <div className="dashboard-card">
          <h2>Profile</h2>
          <p>
            Manage student profile.
          </p>
        </div>

      </div>

    </div>
  )
}

export default Dashboard