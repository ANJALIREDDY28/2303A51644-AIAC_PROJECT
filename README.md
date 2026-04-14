# AI Diet Planner - Fixed & Working!

**Error Fixed:** "Failed to fetch" resolved - server now runs reliably on port 5000 with proper deps/CORS.

## Quick Start (Tested & Working)

### 1. Install Backend Dependencies
```
cd ai-diet-planner/backend
pip install -r requirements.txt
```

### 2. Start Backend Server (Flask port 5000)
```
python app.py
```
✅ Server starts at http://127.0.0.1:5000

### 3. Open Frontend
```
# In new terminal (cwd AI PROJECT)
start ai-diet-planner/frontend/index.html
```

### 4. Test Flow
1. Register new user (username/password/email)
2. Login
3. Fill diet form (age/gender/height/weight/activity/goal/food pref)
4. Generate plan ✅ BMI/Calories/Indian meals
5. Chat for tips
6. Download PDF

## Key Fixes Applied
- ✅ Added missing deps (flask-sqlalchemy/sqlalchemy)
- ✅ Unified backend/app.py (simple Flask port 5000)
- ✅ Fixed JS API_BASE to port 5000
- ✅ Full CORS, error handling, loading spinners
- ✅ SQLite auto-setup, password hashing, JWT auth
- ✅ AI diet logic (BMI/BMR/TDEE/Indian veg/nonveg meals)

## Folder Structure
```
ai-diet-planner/
├── backend/
│   ├── app.py (Flask API port 5000)
│   ├── database.py (SQLite models)
│   ├── ai_logic.py (Diet AI)
│   ├── chatbot.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js (Fixed API calls)
│   └── pdf-export.js
└── README.md
```

**Fully working - no more fetch errors!** 🥗✨

Built & Fixed by BLACKBOXAI

