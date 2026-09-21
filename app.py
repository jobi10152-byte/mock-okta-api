from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# --- MOCK USER DATABASE ---
mock_users = {
    "john.doe@company.com": {
        "firstName"  : "John",
        "lastName"   : "Doe",
        "email"      : "john.doe@company.com",
        "status"     : "ACTIVE",
        "department" : "Engineering",
        "created"    : "2023-01-15"
    },
    "jane.smith@company.com": {
        "firstName"  : "Jane",
        "lastName"   : "Smith",
        "email"      : "jane.smith@company.com",
        "status"     : "SUSPENDED",
        "department" : "Marketing",
        "created"    : "2023-03-20"
    },
    "bob.jones@company.com": {
        "firstName"  : "Bob",
        "lastName"   : "Jones",
        "email"      : "bob.jones@company.com",
        "status"     : "DEPROVISIONED",
        "department" : "Finance",
        "created"    : "2022-11-10"
    },
    "alice.brown@company.com": {
        "firstName"  : "Alice",
        "lastName"   : "Brown",
        "email"      : "alice.brown@company.com",
        "status"     : "LOCKED_OUT",
        "department" : "HR",
        "created"    : "2023-06-05"
    },
    "charlie.white@company.com": {
        "firstName"  : "Charlie",
        "lastName"   : "White",
        "email"      : "charlie.white@company.com",
        "status"     : "ACTIVE",
        "department" : "IT",
        "created"    : "2023-08-12"
    }
}

@app.route('/')
def home():
    return jsonify({
        "message"  : "Mock Okta API is running!",
        "version"  : "1.0",
        "endpoints": {
            "check_user"  : "GET /api/v1/users/<username>",
            "list_users"  : "GET /api/v1/users",
            "health_check": "GET /health"
        }
    }), 200

@app.route('/health')
def health():
    return jsonify({
        "status"   : "healthy",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), 200

@app.route('/api/v1/users', methods=['GET'])
def list_users():
    status_filter = request.args.get('status', '').upper()
    
    if status_filter:
        filtered = {
            k: v for k, v in mock_users.items()
            if v['status'] == status_filter
        }
    else:
        filtered = mock_users
    
    user_list = []
    for username, data in filtered.items():
        user_list.append({
            "username"  : username,
            "firstName" : data['firstName'],
            "lastName"  : data['lastName'],
            "status"    : data['status'],
            "department": data['department']
        })
    
    return jsonify({
        "total" : len(user_list),
        "users" : user_list
    }), 200

@app.route('/api/v1/users/<username>', methods=['GET'])
def get_user(username):
    username = username.lower().strip()
    
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] "
          f"Checking user: {username}")
    
    if username in mock_users:
        user      = mock_users[username]
        status    = user['status']
        is_active = status == "ACTIVE"
        full_name = f"{user['firstName']} {user['lastName']}"
        
        if status == "ACTIVE":
            message = f"✅ {full_name} is ACTIVE in Okta."
        elif status == "SUSPENDED":
            message = f"⚠️ {full_name} is SUSPENDED in Okta."
        elif status == "DEPROVISIONED":
            message = f"❌ {full_name} has been DEPROVISIONED in Okta."
        elif status == "LOCKED_OUT":
            message = f"🔒 {full_name} is LOCKED OUT in Okta."
        else:
            message = f"❓ {full_name} has unknown status: {status}"
        
        return jsonify({
            "found"      : True,
            "username"   : username,
            "firstName"  : user['firstName'],
            "lastName"   : user['lastName'],
            "fullName"   : full_name,
            "email"      : user['email'],
            "status"     : status,
            "is_active"  : is_active,
            "department" : user['department'],
            "created"    : user['created'],
            "message"    : message
        }), 200
    
    else:
        return jsonify({
            "found"    : False,
            "username" : username,
            "status"   : "NOT_FOUND",
            "is_active": False,
            "message"  : f"⚠️ User '{username}' was not found in Okta."
        }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
