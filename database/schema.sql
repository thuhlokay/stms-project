CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL,
    student_number VARCHAR(20) UNIQUE,
    year_level INTEGER,
    course VARCHAR(100),
    campus VARCHAR(100),
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tutor_profiles (
    profile_id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    specialisation VARCHAR(100),
    is_verified BOOLEAN DEFAULT FALSE,
    verified_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE services (
    service_id SERIAL PRIMARY KEY,
    tutor_id INTEGER NOT NULL,
    module_name VARCHAR(100) NOT NULL,
    description TEXT,
    service_type VARCHAR(50),
    duration_minutes INTEGER,
    cost DECIMAL(10, 2),
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (tutor_id) REFERENCES tutor_profiles(profile_id) ON DELETE CASCADE
);

CREATE TABLE tutor_availability (
    availability_id SERIAL PRIMARY KEY,
    tutor_id INTEGER NOT NULL,
    day_of_week VARCHAR(20),
    start_time TIME,
    end_time TIME,
    is_available BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (tutor_id) REFERENCES tutor_profiles(profile_id) ON DELETE CASCADE
);

CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    tutor_id INTEGER NOT NULL,
    start_datetime TIMESTAMP NOT NULL,
    end_datetime TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (service_id) REFERENCES services(service_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (tutor_id) REFERENCES tutor_profiles(profile_id) ON DELETE CASCADE
);