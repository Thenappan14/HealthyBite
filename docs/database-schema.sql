CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE user_profiles (
  id SERIAL PRIMARY KEY,
  user_id INTEGER UNIQUE NOT NULL REFERENCES users(id),
  name VARCHAR(120) NOT NULL,
  age INTEGER NOT NULL,
  sex VARCHAR(50) NOT NULL,
  height_cm FLOAT NOT NULL,
  weight_kg FLOAT NOT NULL,
  activity_level VARCHAR(50) NOT NULL,
  primary_goal VARCHAR(50) NOT NULL,
  diet_type VARCHAR(50) NOT NULL DEFAULT 'none',
  allergies JSONB NOT NULL DEFAULT '[]',
  disliked_foods JSONB NOT NULL DEFAULT '[]',
  spice_preference VARCHAR(50) NOT NULL,
  budget_preference VARCHAR(50) NOT NULL,
  preferred_cuisines JSONB NOT NULL DEFAULT '[]',
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE restaurants (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  website_url VARCHAR(500),
  cuisine_tags JSONB NOT NULL DEFAULT '[]',
  source_type VARCHAR(50) NOT NULL DEFAULT 'url',
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE menus (
  id SERIAL PRIMARY KEY,
  restaurant_id INTEGER REFERENCES restaurants(id),
  source_type VARCHAR(50) NOT NULL,
  source_url VARCHAR(500),
  source_filename VARCHAR(255),
  extracted_text TEXT,
  structured_json JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE menu_items (
  id SERIAL PRIMARY KEY,
  menu_id INTEGER NOT NULL REFERENCES menus(id),
  category VARCHAR(100),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price FLOAT,
  inferred_ingredients JSONB NOT NULL DEFAULT '[]',
  nutrition_estimate JSONB NOT NULL DEFAULT '{}',
  allergens JSONB NOT NULL DEFAULT '[]',
  diet_compatibility JSONB NOT NULL DEFAULT '[]',
  confidence_score FLOAT NOT NULL DEFAULT 0.5,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE recommendations (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  menu_item_id INTEGER NOT NULL REFERENCES menu_items(id),
  recommendation_type VARCHAR(30) NOT NULL DEFAULT 'top_pick',
  match_score FLOAT NOT NULL,
  summary_reason TEXT NOT NULL,
  why_recommended JSONB NOT NULL DEFAULT '[]',
  why_not_recommended JSONB NOT NULL DEFAULT '[]',
  warnings JSONB NOT NULL DEFAULT '[]',
  saved BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE upload_records (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  menu_id INTEGER REFERENCES menus(id),
  file_name VARCHAR(255),
  file_type VARCHAR(50) NOT NULL,
  source_url VARCHAR(500),
  processing_status VARCHAR(50) NOT NULL DEFAULT 'queued',
  notes TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
