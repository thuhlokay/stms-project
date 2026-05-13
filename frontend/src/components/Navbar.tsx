import {
  Link
} from 'react-router-dom'


function Navbar() {

  return (

    <nav className="navbar">

      <div className="logo">
        STMS
      </div>

      <ul className="nav-links">

        <li>
          <Link to="/">
            Home
          </Link>
        </li>

        <li>
          <Link to="/tutors">
            Tutors
          </Link>
        </li>

        <li>
          <Link to="/login">
            Login
          </Link>
        </li>

      </ul>

      <Link to="/register">

        <button className="register-btn">
          Register
        </button>

      </Link>

    </nav>
  )
}

export default Navbar