from my_app import app
# Set host="0.0.0.0" and setup an SSH tunnel from host 127.0.0.1:5000 to
# 0.0.0.0:5000 on the Vagrant VM to allow your browser to interact
# with the Flask development server
app.run(debug=True, host="0.0.0.0")
