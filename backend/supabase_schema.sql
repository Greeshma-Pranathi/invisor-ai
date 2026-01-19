-- Supabase Schema for Invisor.ai
-- Run these commands in your Supabase SQL editor to set up the database

-- Table for storing uploaded CSV files and metadata
CREATE TABLE uploads (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    upload_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    row_count INTEGER NOT NULL,
    column_count INTEGER NOT NULL,
    columns TEXT[] NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for storing churn predictions
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    upload_id INTEGER REFERENCES uploads(id) ON DELETE CASCADE,
    predictions JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for storing customer segments
CREATE TABLE segments (
    id SERIAL PRIMARY KEY,
    upload_id INTEGER REFERENCES uploads(id) ON DELETE CASCADE,
    segments JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for storing explainability results (optional)
CREATE TABLE explanations (
    id SERIAL PRIMARY KEY,
    upload_id INTEGER REFERENCES uploads(id) ON DELETE CASCADE,
    global_importance JSONB,
    individual_explanations JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for better performance
CREATE INDEX idx_uploads_upload_time ON uploads(upload_time);
CREATE INDEX idx_predictions_upload_id ON predictions(upload_id);
CREATE INDEX idx_segments_upload_id ON segments(upload_id);
CREATE INDEX idx_explanations_upload_id ON explanations(upload_id);

-- Enable Row Level Security (RLS) if needed
-- ALTER TABLE uploads ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE segments ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE explanations ENABLE ROW LEVEL SECURITY;

-- Example policies (uncomment if using RLS)
-- CREATE POLICY "Allow all operations for authenticated users" ON uploads
--     FOR ALL USING (auth.role() = 'authenticated');

-- CREATE POLICY "Allow all operations for authenticated users" ON predictions
--     FOR ALL USING (auth.role() = 'authenticated');

-- CREATE POLICY "Allow all operations for authenticated users" ON segments
--     FOR ALL USING (auth.role() = 'authenticated');

-- CREATE POLICY "Allow all operations for authenticated users" ON explanations
--     FOR ALL USING (auth.role() = 'authenticated');