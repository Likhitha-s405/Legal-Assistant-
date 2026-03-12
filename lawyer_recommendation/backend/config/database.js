const mysql = require('mysql2/promise');
const dotenv = require('dotenv');
const path = require('path');

dotenv.config({ path: path.join(__dirname, '../../.env') });

const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'legal_assistant_db',
    port: process.env.DB_PORT || 3306,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0,
    enableKeepAlive: true,
    keepAliveInitialDelay: 0
});

// Test connection
const testConnection = async () => {
    try {
        const connection = await pool.getConnection();
        console.log('✅ Database connected successfully');
        
        // Create tables if they don't exist
        await initializeDatabase(connection);
        
        connection.release();
    } catch (error) {
        console.error('❌ Database connection failed:', error.message);
        // Don't exit, just log error
        console.log('⚠️  Continuing without database connection...');
    }
};

const initializeDatabase = async (connection) => {
    try {
        // Check if tables exist
        const [tables] = await connection.query(`
            CREATE TABLE IF NOT EXISTS practice_areas (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(50) UNIQUE NOT NULL,
                description TEXT,
                icon VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS lawyers (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE,
                phone VARCHAR(20),
                address TEXT,
                latitude DECIMAL(10, 8),
                longitude DECIMAL(11, 8),
                years_experience INT DEFAULT 0,
                rating DECIMAL(2, 1) DEFAULT 0,
                total_reviews INT DEFAULT 0,
                hourly_rate DECIMAL(10, 2),
                bio TEXT,
                profile_image VARCHAR(255),
                is_verified BOOLEAN DEFAULT false,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS lawyer_practice_areas (
                lawyer_id INT,
                practice_area_id INT,
                years_in_area INT,
                PRIMARY KEY (lawyer_id, practice_area_id),
                FOREIGN KEY (lawyer_id) REFERENCES lawyers(id) ON DELETE CASCADE,
                FOREIGN KEY (practice_area_id) REFERENCES practice_areas(id) ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS reviews (
                id INT PRIMARY KEY AUTO_INCREMENT,
                lawyer_id INT,
                user_id INT,
                rating INT CHECK (rating >= 1 AND rating <= 5),
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lawyer_id) REFERENCES lawyers(id) ON DELETE CASCADE
            );
        `);
        
        console.log('✅ Database tables initialized');
        
        // Insert default practice areas if empty
        const [areas] = await connection.query('SELECT COUNT(*) as count FROM practice_areas');
        if (areas[0].count === 0) {
            await connection.query(`
                INSERT INTO practice_areas (name, description) VALUES
                ('Family Law', 'Divorce, child custody, adoption, and family disputes'),
                ('Criminal Law', 'Criminal defense, DUI, and felony cases'),
                ('Corporate Law', 'Business formation, contracts, and mergers'),
                ('Intellectual Property', 'Patents, trademarks, copyrights'),
                ('Real Estate Law', 'Property transactions, landlord-tenant disputes'),
                ('Personal Injury', 'Accident claims, medical malpractice'),
                ('Employment Law', 'Workplace disputes, discrimination, labor rights'),
                ('Tax Law', 'Tax planning, disputes, and compliance'),
                ('Bankruptcy Law', 'Debt relief and bankruptcy filing'),
                ('Immigration Law', 'Visas, green cards, citizenship')
            `);
            console.log('✅ Default practice areas inserted');
        }
        
    } catch (error) {
        console.error('Error initializing database:', error);
    }
};

testConnection();

module.exports = pool;