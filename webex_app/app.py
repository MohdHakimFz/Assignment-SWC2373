from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
WEBEX_API_BASE = 'https://webexapis.com/v1'

# Function to get user info from Webex
def get_user_info(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{WEBEX_API_BASE}/people/me', headers=headers)
    
    if response.status_code == 200:
        user_info = response.json()
        user_info['phoneNumbers'] = user_info.get('phoneNumbers', [])  # Ensure phoneNumbers is always a list
        return user_info
    else:
        return None

# Function to test connection with Webex API
def test_connection(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{WEBEX_API_BASE}/people/me', headers=headers)
    return response.status_code == 200  # Returns True if the connection is successful (status 200)

# Function to get rooms from Webex
def get_rooms(access_token, limit=5):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{WEBEX_API_BASE}/rooms', headers=headers)
    
    if response.status_code == 200:
        rooms = response.json().get('items', [])[:limit]  # Limit the rooms to 'limit' value
        return rooms
    else:
        return None

# Function to delete a room
def delete_room(access_token, room_id):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.delete(f'{WEBEX_API_BASE}/rooms/{room_id}', headers=headers)
    return response.status_code == 204  # Room was deleted successfully

# Function to create a room and add members
def create_room_with_members(access_token, room_title, emails):
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    payload = {'title': room_title}
    
    # Create the room
    response = requests.post(f'{WEBEX_API_BASE}/rooms', headers=headers, json=payload)
    
    if response.status_code == 200:
        room = response.json()
        room_id = room['id']
        
        # Add members to the room
        for email in emails:
            add_member_to_room(access_token, room_id, email)
        
        return room
    else:
        return None

# Function to add a member to the room
def add_member_to_room(access_token, room_id, email):
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    payload = {'roomId': room_id, 'personEmail': email}
    response = requests.post(f'{WEBEX_API_BASE}/memberships', headers=headers, json=payload)
    return response.status_code == 200

# Function to send a message to a room
def send_message_to_room(access_token, room_id, message):
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    payload = {'roomId': room_id, 'text': message}
    response = requests.post(f'{WEBEX_API_BASE}/messages', headers=headers, json=payload)
    return response.status_code == 200

# Function to get members of a room
def get_room_members(access_token, room_id):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{WEBEX_API_BASE}/memberships?roomId={room_id}', headers=headers)
    
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        return []

# Function to get user status
def get_user_status(access_token, email):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{WEBEX_API_BASE}/people?email={email}', headers=headers)
    
    if response.status_code == 200:
        person = response.json().get('items', [])[0]
        return {'status': person.get('status', 'unknown')}  # active, inactive, dnd, etc.
    else:
        return None

# Index route for entering access token
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        access_token = request.form.get('access_token')
        user_info = get_user_info(access_token)
        if user_info:
            return redirect(url_for('menu', access_token=access_token))
        else:
            return "Invalid access token. Please try again.", 400
    return render_template('index.html')

# Menu route
@app.route('/menu/<access_token>', methods=['GET'])
def menu(access_token):
    rooms = get_rooms(access_token)
    return render_template('menu.html', access_token=access_token, rooms=rooms)

# Route to test connection (Option 0)
@app.route('/test_connection/<access_token>', methods=['GET'])
def test_conn(access_token):
    if test_connection(access_token):
        message = "Connection successful!"
    else:
        message = "Connection failed."
    return render_template('connection_status.html', message=message, access_token=access_token)

# Route to user info (Option 1)
@app.route('/user_info/<access_token>', methods=['GET'])
def user_info(access_token):
    user_info = get_user_info(access_token)
    if user_info:
        return render_template('user_info.html', user_info=user_info)
    else:
        return "Failed to retrieve user info.", 400

# Route to display (Option 2)
@app.route('/rooms/<access_token>', methods=['GET'])
def rooms(access_token):
    rooms = get_rooms(access_token)
    if rooms:
        return render_template('rooms.html', rooms=rooms, access_token=access_token)
    else:
        return "Failed to retrieve rooms.", 400

# Route to display room and delete function (Option 2)
@app.route('/delete_room_from_list/<access_token>/<room_id>', methods=['POST'])
def delete_room_from_list(access_token, room_id):
    if delete_room(access_token, room_id):
        return redirect(url_for('rooms', access_token=access_token))
    else:
        return "Failed to delete room.", 400

# Route to create a room with members (Option 3)
@app.route('/create_room/<access_token>', methods=['GET', 'POST'])
def create_room_route(access_token):
    if request.method == 'POST':
        room_title = request.form.get('room_title')
        emails = request.form.get('emails').split(',')  # Assuming emails are comma-separated
        
        if room_title and emails:
            room = create_room_with_members(access_token, room_title, emails)
            if room:
                # Render a success template with room details
                return render_template('success.html', room_title=room_title, access_token=access_token)
            else:
                return "Failed to create room.", 400
        else:
            return "Room title and emails cannot be empty.", 400
    return render_template('create_room.html', access_token=access_token)


# Route to send a message to a room
@app.route('/send_message/<access_token>', methods=['GET', 'POST'])
def send_message(access_token):
    rooms = get_rooms(access_token)
    if not rooms:
        return "No rooms available to send a message.", 400

    if request.method == 'POST':
        room_id = request.form.get('room_id')
        message = request.form.get('message')
        if room_id and message:
            if send_message_to_room(access_token, room_id, message):
                return redirect(url_for('menu', access_token=access_token))
            else:
                return "Failed to send message.", 400
        else:
            return "Room and message cannot be empty.", 400
    return render_template('send_message.html', rooms=rooms, access_token=access_token)

# Route to display group members' status
@app.route('/group_status/<access_token>/<room_id>', methods=['GET'])
def group_status(access_token, room_id):
    members = get_room_members(access_token, room_id)
    members_status = []
    for member in members:
        status = get_user_status(access_token, member['personEmail'])
        if status:
            members_status.append({
                'displayName': member['personDisplayName'],
                'status': status['status']
            })
    return render_template('group_status.html', members_status=members_status, access_token=access_token)


# List Room
@app.route('/list_rooms/<access_token>', methods=['GET'])
def list_rooms(access_token):
    rooms = get_rooms(access_token)
    if rooms:
        return render_template('list_rooms.html', rooms=rooms, access_token=access_token)
    else:
        return "Failed to retrieve rooms.", 400

# Route to logout
@app.route('/logout', methods=['GET'])
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
