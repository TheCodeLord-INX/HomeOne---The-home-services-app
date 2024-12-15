from Project import create_app
app = create_app()

# import os
# from flask import Flask
# def create_app():
#     # Create Flask application
#     app = Flask(__name__)
#     # Ensure the 'instance' folder exists
#     os.makedirs(app.instance_path, exist_ok=True)
#     # Paths for the database files
#     db1_path = os.path.join(app.instance_path, 'db1.sqlite')
#     db2_path = os.path.join(app.instance_path, 'db2.sqlite')
#     # Create the database files if they don't exist
#     open(db1_path, 'a').close()  # Create empty file
#     open(db2_path, 'a').close()  # Create empty file
#     print(f"Database 1 created at: {db1_path}")
#     print(f"Database 2 created at: {db2_path}")
#     return app

# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)


if __name__ == "__main__":
    # app.run(host='', port=5000, debug=True)
    app.run(debug=True)