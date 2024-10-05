# Webex Application

## Description
This project is a Webex application built with Flask that enables users to manage rooms, send messages, and check the status of users in a collaborative environment. The application interacts with the Webex API, providing functionalities such as creating rooms, adding members, sending messages, and retrieving user information.

## Features
- **User Authentication**: Enter your Webex access token to start using the application.
- **Room Management**: Create new rooms, view existing rooms, and delete rooms.
- **Send Messages**: Send messages to specific rooms.
- **User Status**: Check the status of users in the rooms.
- **Display Group Members' Status**: View the online status of all members in a specified room.

## Technologies Used
- **Python**: Programming language used for application development.
- **Flask**: Web framework for building the application.
- **Webex API**: API for interacting with Webex services.
- **HTML/CSS**: For front-end templates and styling.
- **Requests Library**: For making HTTP requests to the Webex API.

## Installation

### Step 1: Clone the Repository
1. Open your terminal (Command Prompt, PowerShell, or Terminal).
2. Clone the repository using the following command:
   ```bash
   git clone https://github.com/yourusername/webex-app.git
   ```
3. Navigate into the project directory:
   ```bash
   cd webex-app
   ```

### Step 2: Set Up a Virtual Environment
Setting up a virtual environment is a best practice to manage dependencies:
1. Create a virtual environment:
   ```bash
   # For Windows
   py -3 -m venv {anyfoldername} 
   . {anyfoldername}/Scripts/activate 

   # For macOS/Linux
   python3 -m venv  {anyfoldername} 
   . {anyfoldername}/Scripts/activate 
   ```

### Step 3: Install Flask and Requests
Install the required packages (Flask and Requests) using pip:
```bash
pip install Flask
pip install requests
```

### Step 4: Run the Application
Start the Flask application by executing:
```bash
python app.py
```

### Step 5: Access the Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```
You should see the landing page for the Webex application.

## Usage Instructions
1. **Enter Access Token**: 
   - On the landing page, input your Webex access token to authenticate.
2. **Navigate the Menu**:
   - After entering a valid token, you will be redirected to the menu where you can access various features:
     - **Check Rooms**: View a list of your rooms.
     - **Send Messages**: Choose a room and send a message.
     - **User Status**: Check the status of users.
3. **Create Rooms**:
   - Use the "Create Room" option to create a new room and add members by entering their email addresses.
4. **Delete Rooms**:
   - Select a room to delete it from your list.
5. **Send Messages**:
   - Choose a room and type a message to send it to the selected room.
6. **Display Group Members' Status**:
   - View the online status of all members in a specified room.

## API Reference
For further details on the Webex API, you can refer to the official documentation:
- [Webex API Documentation](https://developer.webex.com/docs/api/v1/overview)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- **Flask**: [Flask Documentation](https://flask.palletsprojects.com/en/2.0.x/) for the web framework.
- **Webex API**: [Webex API Documentation](https://developer.webex.com/docs/api/v1/overview) for the integration capabilities.
- Thanks to all contributors and the community for their support and resources.

## Contributing
If you would like to contribute to this project:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to your forked repository.
4. Submit a pull request.

Please ensure your code adheres to the project's style guidelines and includes appropriate tests.

## Contact
For any inquiries or issues, please contact me at kl2307014329@student.uptm.edu.my


This README is structured to provide clear and thorough guidance, making it easier for others to understand, set up, and contribute to your Webex application project. If you need further modifications or additional sections, feel free to let me know!
