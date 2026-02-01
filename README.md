.

🗳️ Online Voting System (Flask + SQLite)

A full-stack Online Voting System built using Flask (Python) for the backend and HTML, CSS, JavaScript for the frontend.
This project supports secure voting, admin management, real-time results, and analytics.

🚀 Features
👤 Voter Features

View list of candidates with images

Vote only once using voter ID

Real-time vote confirmation

View election results & statistics

🧑‍💼 Admin Features

Admin login

Add new candidates

View all voters

Reset election data

View system statistics & voting trends

📊 Analytics

Total votes & voters

Voting percentage

Leading candidate

Voting timeline (last 7 days)

Most active voting hour

🛠️ Tech Stack
Layer	Technology
Backend	Python, Flask
Database	SQLite
Frontend	HTML, CSS, JavaScript
API Style	REST API
Others	Flask-CORS
📂 Project Structure
online-voting-system/
│
├── voting.py          # Flask backend
├── voting.db          # SQLite database (auto-generated)
├── index.html         # Frontend UI
├── README.md          # Project documentation

2️⃣ Install Dependencies
pip install flask flask-cors

3️⃣ Run the Backend Server
python voting.py


Server will start at:

http://localhost:5000

🌐 API Endpoints
Endpoint	Method	Description
/api/candidates	GET	Get all candidates
/api/vote	POST	Submit a vote
/api/results	GET	Get election results
/api/stats	GET	Get system statistics
/api/voter/<id>	GET	Check voter status
/api/admin/login	POST	Admin login
/api/admin/reset	POST	Reset election
/api/health	GET	Health check
🔐 Admin Credentials (Demo)
Username: admin
Password: admin123


⚠️ For demo/college use only. Passwords are not encrypted.

🖼️ Screenshots
<img width="1897" height="888" alt="Screenshot 2026-02-01 195550" src="https://github.com/user-attachments/assets/60ea453f-bbd5-4289-aa8f-e1766e4bc7bd" />
<img width="1894" height="879" alt="Screenshot 2026-02-01 195605" src="https://github.com/user-attachments/assets/707ca003-83be-43cb-9c36-c68bcb49fcd2" />
<img width="1890" height="877" alt="Screenshot 2026-02-01 195702" src="https://github.com/user-attachments/assets/95b03b9b-1b44-4816-896a-83059424c5e3" />
<img width="1895" height="881" alt="Screenshot 2026-02-01 195746" src="https://github.com/user-attachments/assets/71761db3-40f2-4ff2-b0be-24b4b805e5bd" />
<img width="1897" height="877" alt="Screenshot 2026-02-01 195806" src="https://github.com/user-attachments/assets/fd321733-7341-418d-9be2-c8d103862be1" />
<img width="1896" height="879" alt="Screenshot 2026-02-01 195828" src="https://github.com/user-attachments/assets/f85f45c3-d55d-47a1-978d-355a9b67edea" />
<img width="1890" height="876" alt="Screenshot 2026-02-01 195851" src="https://github.com/user-attachments/assets/5e6ae3a0-0ef2-4560-88e5-ec9ca91b4a79" />
<img width="1885" height="876" alt="Screenshot 2026-02-01 195910" src="https://github.com/user-attachments/assets/c2b2e36f-04a3-4b16-9550-bd8c5416714c" />


👨‍💻 Author

ASWINI
Department of Computer Science
VSB COLLEGE OF ENINEERING TECHNICAL CAMPUS COIMBATORE

📄 License

This project is for educational purposes only.
