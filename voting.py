"""
COMPLETE ONLINE VOTING SYSTEM BACKEND
File: voting.py
Run: python voting.py
"""
from flask import Flask, jsonify, request, g, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import json
from datetime import datetime

# ========== FLASK APP INITIALIZATION ==========
app = Flask(__name__)
CORS(app)

# ========== DATABASE CONFIGURATION ==========
DATABASE = 'voting.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

app.teardown_appcontext(close_db)

def dict_from_row(row):
    return dict(zip(row.keys(), row)) if row else None

# ========== DATABASE INITIALIZATION WITH IMAGES ==========
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('DROP TABLE IF EXISTS candidates')
        cursor.execute('DROP TABLE IF EXISTS voters')
        cursor.execute('DROP TABLE IF EXISTS admin')
        cursor.execute('DROP TABLE IF EXISTS votes_log')
        
        cursor.execute('''
            CREATE TABLE candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                party TEXT NOT NULL,
                bio TEXT,
                color TEXT,
                votes INTEGER DEFAULT 0,
                avatar TEXT,
                image_url TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE voters (
                id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                has_voted BOOLEAN DEFAULT 0,
                vote_time TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE admin (
                username TEXT PRIMARY KEY,
                password TEXT,
                email TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE votes_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voter_id TEXT,
                candidate_id INTEGER,
                vote_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        admin_data = [
            ('admin', 'admin123', 'admin@voting.com'),
            ('supervisor', 'super123', 'supervisor@voting.com'),
            ('manager', 'manager123', 'manager@voting.com')
        ]
        cursor.executemany(
            'INSERT INTO admin (username, password, email) VALUES (?, ?, ?)',
            admin_data
        )
        
        # CANDIDATES WITH REAL IMAGE URLs
        dummy_candidates = [
            ('John Smith', 'Democratic Party', 
             'Former mayor with 10 years experience in public service. Focuses on education reform and healthcare.',
             '#2196F3', 156, '👨‍💼', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face'),
            
                       ('Sarah Johnson', 'Republican Alliance', 
             'Business leader and philanthropist. Advocates for economic growth and job creation.',
             '#F44336', 142, '👩‍💼', 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face'),
            
            ('Michael Chen', 'Progressive Movement', 
             'Environmental scientist pushing for green energy and climate change policies.',
             '#4CAF50', 98, '👨‍🔬', 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&h=400&fit=crop&crop=face'),
            
            ('Emma Williams', 'Unity Coalition', 
             'Human rights lawyer focused on social justice and equality for all citizens.',
             '#FF9800', 87, '👩‍⚖️', 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop&crop=face'),
            
            ('David Brown', 'Tech Future Party', 
             'Tech entrepreneur advocating for digital transformation and innovation in government.',
             '#9C27B0', 76, '👨‍💻', 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face'),
            
            ('Lisa Garcia', 'Green Party', 
             'Environmental activist with plans for sustainable cities and conservation.',
             '#00BCD4', 65, '👩‍🌾', 'https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?w=400&h=400&fit=crop&crop=face'),
            
            ('Robert Wilson', 'Conservative Union', 
             'Military veteran focused on national security and traditional values.',
             '#795548', 54, '👨‍✈️', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop&crop=face'),
            
            ('Maria Rodriguez', 'People\'s Choice', 
             'Community organizer working on affordable housing and local businesses.',
             '#FF5722', 43, '👩‍🏫', 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&h=400&fit=crop&crop=face')
        ]
        
        cursor.executemany(
            'INSERT INTO candidates (name, party, bio, color, votes, avatar, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)',
            dummy_candidates
        )
        
        voter_names = [
            'James Miller', 'Patricia Davis', 'Jennifer Wilson', 'William Taylor',
            'Elizabeth Moore', 'David Anderson', 'Barbara Thomas', 'Richard Jackson',
            'Susan White', 'Joseph Harris', 'Margaret Martin', 'Charles Thompson',
            'Jessica Garcia', 'Thomas Martinez', 'Sarah Robinson', 'Daniel Clark',
            'Karen Lewis', 'Matthew Lee', 'Nancy Walker', 'Anthony Hall',
            'Betty Allen', 'Mark Young', 'Dorothy Hernandez', 'Steven King',
            'Sandra Wright', 'Paul Lopez', 'Ashley Hill', 'George Scott',
            'Kimberly Green', 'Kenneth Adams', 'Emily Baker', 'Joshua Gonzalez',
            'Donna Nelson', 'Kevin Carter', 'Michelle Mitchell', 'Brian Perez',
            'Carol Roberts', 'Edward Turner', 'Amanda Phillips', 'Ronald Campbell',
            'Melissa Parker', 'Jason Evans', 'Deborah Edwards', 'Jeffrey Collins',
            'Stephanie Stewart', 'Ryan Sanchez', 'Rebecca Morris', 'Jacob Rogers',
            'Laura Reed', 'Gary Cook', 'Donna Morgan', 'Nicholas Bell',
            'Cynthia Murphy', 'Eric Bailey', 'Angela Rivera', 'Jonathan Cooper',
            'Brenda Richardson', 'Stephen Cox', 'Pamela Howard', 'Larry Ward',
            'Sharon Torres', 'Scott Peterson', 'Katherine Gray', 'Brandon Ramirez',
            'Amy James', 'Benjamin Watson', 'Ruth Brooks', 'Samuel Kelly',
            'Virginia Sanders', 'Gregory Price', 'Kathleen Bennett', 'Frank Wood',
            'Alice Barnes', 'Raymond Ross', 'Diane Henderson', 'Patrick Coleman',
            'Janice Jenkins', 'Alexander Perry', 'Cheryl Powell', 'Jack Long',
            'Martha Patterson', 'Dennis Hughes', 'Gloria Flores', 'Jerry Washington',
            'Evelyn Butler', 'Tyler Simmons', 'Joan Foster', 'Aaron Gonzales',
            'Judith Bryant', 'Henry Alexander', 'Megan Russell', 'Carl Griffin',
            'Andrea Diaz', 'Arthur Hayes', 'Marie Myers', 'Lawrence Ford'
        ]
        
        voters_data = []
        for i, name in enumerate(voter_names, 1):
            voter_id = f'VOTER{str(i).zfill(3)}'
            email = f'voter{i}@email.com'
            has_voted = 1 if i <= 60 else 0
            voters_data.append((voter_id, name, email, has_voted, datetime.now().isoformat() if has_voted else None))
        
        cursor.executemany(
            'INSERT INTO voters (id, name, email, has_voted, vote_time) VALUES (?, ?, ?, ?, ?)',
            voters_data
        )
        
        votes_log_data = []
        candidate_ids = list(range(1, 9))
        
        for voter_num in range(1, 61):
            voter_id = f'VOTER{str(voter_num).zfill(3)}'
            if voter_num <= 15:
                candidate_id = 1
            elif voter_num <= 30:
                candidate_id = 2
            elif voter_num <= 40:
                candidate_id = 3
            elif voter_num <= 47:
                candidate_id = 4
            elif voter_num <= 53:
                candidate_id = 5
            elif voter_num <= 58:
                candidate_id = 6
            elif voter_num <= 59:
                candidate_id = 7
            else:
                candidate_id = 8
            
            votes_log_data.append((voter_id, candidate_id, datetime.now().isoformat()))
        
        cursor.executemany(
            'INSERT INTO votes_log (voter_id, candidate_id, vote_time) VALUES (?, ?, ?)',
            votes_log_data
        )
        
        db.commit()
        print("✅ Database initialized with candidate images!")

# ========== API ENDPOINTS ==========

@app.route('/')
def home():
    return jsonify({
        'message': 'Online Voting System Backend',
        'status': 'running',
        'version': '3.0',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            '/api/candidates': 'GET - Get all candidates',
            '/api/vote': 'POST - Submit a vote',
            '/api/results': 'GET - Get election results',
            '/api/voter/<voter_id>': 'GET - Check voter status',
            '/api/stats': 'GET - Get system statistics',
            '/api/admin/login': 'POST - Admin login',
            '/api/admin/candidates': 'POST - Add new candidate',
            '/api/admin/reset': 'POST - Reset election',
            '/api/health': 'GET - Health check'
        }
    })

@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM candidates ORDER BY votes DESC')
        rows = cursor.fetchall()
        
        candidates = [dict_from_row(row) for row in rows]
        return jsonify(candidates)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vote', methods=['POST'])
def vote():
    try:
        data = request.json
        candidate_id = data.get('candidate_id')
        voter_id = data.get('voter_id')
        
        if not candidate_id or not voter_id:
            return jsonify({'error': 'Candidate ID and Voter ID are required'}), 400
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT has_voted FROM voters WHERE id = ?', (voter_id,))
        voter = cursor.fetchone()
        
        if voter:
            if voter['has_voted']:
                return jsonify({'error': 'This voter has already voted!'}), 403
        else:
            cursor.execute(
                'INSERT INTO voters (id, name, email, has_voted) VALUES (?, ?, ?, ?)',
                (voter_id, f'Voter {voter_id}', f'{voter_id}@email.com', 0)
            )
        
        cursor.execute('SELECT id FROM candidates WHERE id = ?', (candidate_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Candidate not found'}), 404
        
        cursor.execute('UPDATE candidates SET votes = votes + 1 WHERE id = ?', (candidate_id,))
        
        vote_time = datetime.now().isoformat()
        cursor.execute(
            'UPDATE voters SET has_voted = 1, vote_time = ? WHERE id = ?',
            (vote_time, voter_id)
        )
        
        cursor.execute(
            'INSERT INTO votes_log (voter_id, candidate_id, vote_time) VALUES (?, ?, ?)',
            (voter_id, candidate_id, vote_time)
        )
        
        db.commit()
        
        cursor.execute('SELECT * FROM candidates WHERE id = ?', (candidate_id,))
        candidate = dict_from_row(cursor.fetchone())
        
        return jsonify({
            'success': True,
            'message': 'Vote recorded successfully!',
            'timestamp': vote_time,
            'candidate': {
                'id': candidate['id'],
                'name': candidate['name'],
                'party': candidate['party'],
                'votes': candidate['votes']
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/results', methods=['GET'])
def get_results():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM candidates ORDER BY votes DESC')
        rows = cursor.fetchall()
        
        candidates = [dict_from_row(row) for row in rows]
        total_votes = sum(candidate['votes'] for candidate in candidates)
        
        for candidate in candidates:
            percentage = (candidate['votes'] / total_votes * 100) if total_votes > 0 else 0
            candidate['percentage'] = round(percentage, 2)
        
        cursor.execute('SELECT COUNT(*) as total FROM voters')
        total_voters = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as voted FROM voters WHERE has_voted = 1')
        voted_count = cursor.fetchone()['voted']
        
        cursor.execute('''
            SELECT DATE(vote_time) as date, COUNT(*) as votes 
            FROM votes_log 
            WHERE vote_time IS NOT NULL 
            GROUP BY DATE(vote_time) 
            ORDER BY date DESC 
            LIMIT 7
        ''')
        timeline = [dict_from_row(row) for row in cursor.fetchall()]
        
        return jsonify({
            'candidates': candidates,
            'summary': {
                'total_votes': total_votes,
                'total_voters': total_voters,
                'voted_count': voted_count,
                'voting_percentage': round((voted_count / total_voters * 100), 2) if total_voters > 0 else 0,
                'leading_candidate': candidates[0]['name'] if candidates else 'None',
                'timestamp': datetime.now().isoformat()
            },
            'timeline': timeline
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM candidates')
        candidate_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM voters')
        voter_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM votes_log')
        vote_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM voters WHERE has_voted = 1')
        voted_count = cursor.fetchone()['count']
        
        cursor.execute('''
            SELECT strftime('%H', vote_time) as hour, COUNT(*) as votes
            FROM votes_log 
            WHERE vote_time IS NOT NULL
            GROUP BY hour
            ORDER BY votes DESC
            LIMIT 1
        ''')
        most_active = cursor.fetchone()
        
        return jsonify({
            'statistics': {
                'candidates': candidate_count,
                'voters': voter_count,
                'total_votes': vote_count,
                'voters_voted': voted_count,
                'voting_rate': round((voted_count / voter_count * 100), 2) if voter_count > 0 else 0,
                'most_active_hour': most_active['hour'] if most_active else 'N/A'
            },
            'system': {
                'database': DATABASE,
                'status': 'running',
                'timestamp': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voter/<voter_id>', methods=['GET'])
def get_voter_status(voter_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM voters WHERE id = ?', (voter_id,))
        voter = cursor.fetchone()
        
        if voter:
            return jsonify(dict_from_row(voter))
        else:
            return jsonify({
                'id': voter_id,
                'name': f'Voter {voter_id}',
                'email': f'{voter_id}@email.com',
                'has_voted': False,
                'vote_time': None,
                'is_new': True
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'SELECT * FROM admin WHERE username = ? AND password = ?',
            (username, password)
        )
        admin = cursor.fetchone()
        
        if admin:
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'admin': dict_from_row(admin),
                'token': f'admin_token_{username}_{datetime.now().timestamp()}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/candidates', methods=['POST'])
def add_candidate():
    try:
        data = request.json
        name = data.get('name')
        party = data.get('party')
        bio = data.get('bio', '')
        color = data.get('color', '#FF6B6B')
        avatar = data.get('avatar', '👤')
        image_url = data.get('image_url')
        
        if not name or not party:
            return jsonify({'error': 'Name and party are required'}), 400
        
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute(
            'INSERT INTO candidates (name, party, bio, color, avatar, image_url, votes) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (name, party, bio, color, avatar, image_url, 0)
        )
        db.commit()
        
        candidate_id = cursor.lastrowid
        cursor.execute('SELECT * FROM candidates WHERE id = ?', (candidate_id,))
        new_candidate = dict_from_row(cursor.fetchone())
        
        return jsonify({
            'success': True,
            'message': 'Candidate added successfully',
            'candidate': new_candidate
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/voters', methods=['GET'])
def get_all_voters():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM voters ORDER BY id')
        rows = cursor.fetchall()
        
        voters = [dict_from_row(row) for row in rows]
        return jsonify(voters)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/reset', methods=['POST'])
def reset_election():
    try:
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('UPDATE candidates SET votes = 0')
        cursor.execute('UPDATE voters SET has_voted = 0, vote_time = NULL')
        cursor.execute('DELETE FROM votes_log')
        
        votes_data = []
        for i in range(1, 61):
            voter_id = f'VOTER{str(i).zfill(3)}'
            candidate_id = (i % 8) + 1
            votes_data.append((voter_id, candidate_id, datetime.now().isoformat()))
        
        cursor.executemany(
            'INSERT INTO votes_log (voter_id, candidate_id, vote_time) VALUES (?, ?, ?)',
            votes_data[:30]
        )
        
        for candidate_id in range(1, 9):
            vote_count = len([v for v in votes_data[:30] if v[1] == candidate_id])
            if vote_count > 0:
                cursor.execute(
                    'UPDATE candidates SET votes = votes + ? WHERE id = ?',
                    (vote_count, candidate_id)
                )
        
        for i in range(1, 31):
            voter_id = f'VOTER{str(i).zfill(3)}'
            cursor.execute(
                'UPDATE voters SET has_voted = 1, vote_time = ? WHERE id = ?',
                (datetime.now().isoformat(), voter_id)
            )
        
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Election reset with 30 dummy votes',
            'votes_added': 30
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT 1')
        
        cursor.execute('SELECT COUNT(*) as count FROM candidates')
        candidates = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM voters')
        voters = cursor.fetchone()['count']
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'tables': {
                'candidates': candidates,
                'voters': voters,
                'votes_log': 'present',
                'admin': 'present'
            },
            'timestamp': datetime.now().isoformat(),
            'uptime': 'running'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500

# ========== APPLICATION START ==========
if __name__ == '__main__':
    print("=" * 60)
    print("ONLINE VOTING SYSTEM BACKEND - WITH CANDIDATE IMAGES")
    print("=" * 60)
    print("Initializing database with candidate images...")
    
    init_db()
    
    print("\n✅ Ready! Your backend has been populated with:")
    print("   • 8 Candidates with images from Unsplash")
    print("   • 100 Voters (60 already voted)")
    print("   • 60 Vote records")
    print("   • 3 Admin accounts")
    print("\n📊 Admin Login Credentials:")
    print("   Username: admin, Password: admin123")
    print("\n🌐 Available Endpoints:")
    print("   • http://localhost:5000/")
    print("   • http://localhost:5000/api/candidates")
    print("   • http://localhost:5000/api/results")
    print("   • http://localhost:5000/api/stats")
    print("   • http://localhost:5000/api/health")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, port=5000)