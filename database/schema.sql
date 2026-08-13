CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE users (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 email VARCHAR(255) UNIQUE,
 phone VARCHAR(20) UNIQUE,
 password_hash TEXT,
 role VARCHAR(30) NOT NULL DEFAULT 'user',
 is_active BOOLEAN DEFAULT TRUE,
 is_verified BOOLEAN DEFAULT FALSE,
 preferred_language VARCHAR(10) DEFAULT 'en',
 created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
 updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE profiles (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 full_name VARCHAR(200), date_of_birth DATE, gender VARCHAR(30),
 address TEXT, district VARCHAR(100), state VARCHAR(100), pincode VARCHAR(10),
 profile_photo_url TEXT,
 created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
 updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE services (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 name VARCHAR(200) NOT NULL, category VARCHAR(100), description TEXT,
 official_authority VARCHAR(255), official_url TEXT, application_url TEXT,
 service_type VARCHAR(30) DEFAULT 'official',
 government_fee NUMERIC(12,2) DEFAULT 0, service_fee NUMERIC(12,2) DEFAULT 0,
 processing_information TEXT, is_active BOOLEAN DEFAULT TRUE,
 last_verified_at TIMESTAMPTZ, created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE applications (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 service_id UUID NOT NULL REFERENCES services(id),
 application_number VARCHAR(100) UNIQUE,
 status VARCHAR(50) DEFAULT 'submitted', next_action TEXT, notes TEXT,
 submitted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
 updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE documents (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 application_id UUID REFERENCES applications(id) ON DELETE SET NULL,
 document_type VARCHAR(100) NOT NULL, original_filename VARCHAR(255),
 storage_path TEXT, mime_type VARCHAR(100), file_size BIGINT,
 created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE document_expiry (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
 document_type VARCHAR(100), expiry_date DATE NOT NULL,
 reminder_90_sent BOOLEAN DEFAULT FALSE, reminder_60_sent BOOLEAN DEFAULT FALSE,
 reminder_30_sent BOOLEAN DEFAULT FALSE, reminder_7_sent BOOLEAN DEFAULT FALSE,
 created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payments (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 application_id UUID REFERENCES applications(id) ON DELETE SET NULL,
 government_fee NUMERIC(12,2) DEFAULT 0, service_fee NUMERIC(12,2) DEFAULT 0,
 total_amount NUMERIC(12,2) NOT NULL, payment_status VARCHAR(50) DEFAULT 'pending',
 gateway VARCHAR(100), transaction_id VARCHAR(255), receipt_url TEXT,
 created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notifications (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 title VARCHAR(255) NOT NULL, message TEXT NOT NULL,
 notification_type VARCHAR(100), is_read BOOLEAN DEFAULT FALSE,
 created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE support_tickets (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 subject VARCHAR(255), description TEXT, status VARCHAR(50) DEFAULT 'open',
 priority VARCHAR(30) DEFAULT 'normal', assigned_staff_id UUID,
 created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
 updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE staff (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,
 department VARCHAR(100), is_active BOOLEAN DEFAULT TRUE,
 created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE admins (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,
 created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE service_providers (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,
 organization_name VARCHAR(255), is_verified BOOLEAN DEFAULT FALSE,
 created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE appointments (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
 application_id UUID REFERENCES applications(id) ON DELETE SET NULL,
 appointment_date TIMESTAMPTZ NOT NULL, location TEXT,
 status VARCHAR(50) DEFAULT 'scheduled',
 created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE job_listings (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 title VARCHAR(255) NOT NULL, company VARCHAR(255), category VARCHAR(100),
 job_type VARCHAR(100), location VARCHAR(255), description TEXT,
 application_url TEXT, is_active BOOLEAN DEFAULT TRUE,
 created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
 id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
 user_id UUID REFERENCES users(id) ON DELETE SET NULL,
 action VARCHAR(255) NOT NULL, entity_type VARCHAR(100), entity_id UUID,
 ip_address VARCHAR(100), created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
