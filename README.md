🗳️ Online Voting System
A secure, full-stack online voting system built with Python Flask backend and HTML/CSS/JS frontend.



🌐 Live Demo
Frontend (Voting Interface): https://github.com/Aswini-ox/online-voting-system.git

Backend API: https://blossomless-stefany-rancid.ngrok-free.dev/api (temporary, changes every 2 hours)

📋 Features
✅ User Features:

Secure voter login system

Beautiful candidate cards with images

One vote per voter prevention

Live results with animated charts

Mobile-responsive design

✅ Admin Features:

Admin authentication panel

Add/remove candidates

Reset entire election

View voting statistics

Export election data

✅ Technical Features:

SQLite database with dummy data

RESTful API endpoints

CORS enabled for frontend-backend communication

Gradient UI with hover animations
Quick Start
1. Clone & Setup
bash
# Clone repository
git clone https://github.com/yourusername/online-voting-system.git
cd online-voting-system

# Install Python dependencies
pip install flask flask-cors
2. Run Backend Server
bash
python voting.py
Backend starts at: http://localhost:5000

3. Open Frontend
Simply open online.html in any modern browser.

📁 Project Structure
text
online-voting-system/
├── voting.py              # Flask backend server (23KB)
├── online.html           # Complete frontend - HTML/CSS/JS (60KB)
├── README.md            # This documentation file
├── requirements.txt     # Python dependencies (optional)
└── voting.db           # SQLite database (auto-generated)
👥 Usage Guide
For Voters:
Open online.html in browser

Click "Vote Now" tab

Login with any NEW Voter ID (e.g., VOTER101, NEWUSER001)

Select your preferred candidate

View live results instantly

For Admins:
Access: https://blossomless-stefany-rancid.ngrok-free.dev

Login with: admin / admin123

Manage candidates, reset elections, view stats

Demo Credentials:
Already Voted: VOTER001 to VOTER100 (60 users)

New Voters: Use any new ID like TEST001, FRIEND001

Admin: admin / admin123

Supervisor: supervisor / super123

Manager: manager / manager123

🛠️ Deployment
1. Temporary Public Access (ngrok):
bash
# Start Flask backend
python voting.py

# In NEW terminal, start ngrok tunnel
ngrok config add-authtoken YOUR_TOKEN
ngrok http 5000
Copy the https://*.ngrok-free.dev URL shown.

2. Permanent Frontend (GitHub Pages):
Upload online.html to GitHub repository

Enable GitHub Pages in Settings → Pages

Your site: https://username.github.io/repository-name/

3. Update Frontend Connection:
In online.html, change line 87:

javascript
// Change this:
const API_BASE = 'http://localhost:5000/api';
// To your ngrok URL:
const API_BASE = 'https://blossomless-stefany-rancid.ngrok-free.dev/api';
🎨 UI Features
Gradient Background: Orange (#f5af19) to Red (#f12711)

Animated Cards: Hover effects and transitions

Live Progress Bars: Animated voting percentages

Candidate Images: Real photos from Unsplash

Party Symbols: Color-coded with icons

Responsive Design: Works perfectly on mobile/tablet/desktop
📚 Tech Stack
Backend: Python 3.9+, Flask, SQLite

Frontend: HTML5, CSS3, Vanilla JavaScript

Database: SQLite with direct SQL execution

Deployment: Ngrok (tunnel), GitHub Pages (frontend hosting)

Styling: Custom CSS with gradients, animations, Flexbox/Grid

Icons: Font Awesome 6.4.0

Demo Images: Unsplash (attribution-free)

👨‍💻 Development Notes
File Details:
voting.py (23,005 bytes): Complete Flask backend with:

Database initialization with dummy data

8 API endpoints + admin functions

SQLite connection management

CORS configuration for frontend access

online.html (59,845 bytes): Single-file frontend with:

4 pages: Home, Vote, Results, Admin

600+ lines of CSS with animations

400+ lines of JavaScript with API integration

Responsive design for all screen sizes

Database Schema:
sql
candidates (id, name, party, bio, color, votes, avatar, image_url)
voters (id, name, email, has_voted, vote_time)
admin (username, password, email)
votes_log (id, voter_id, candidate_id, vote_time)
🤝 How to Contribute
Fork this repository

Create a feature branch: git checkout -b feature-name

Make your changes

Test thoroughly

Submit a Pull Request

🙏 Acknowledgments
Icons by Font Awesome

Demo images from Unsplash

Gradient inspiration from modern web design trends

ngrok for easy tunneling solution


Keep Servers Running: Remember to keep both Flask and ngrok terminals open
