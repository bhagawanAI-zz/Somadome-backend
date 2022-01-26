from app import app
# from db import db
# from ma import ma

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    from db import db
    from ma import ma
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000)