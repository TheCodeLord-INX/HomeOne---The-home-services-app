from Project import create_app

app = create_app()

if __name__ == "__main__":
    # app.run(host='', port=5000, debug=True)
    app.run(debug=True)