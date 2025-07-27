from api.app import app

# Vercel 需要的應用實例
application = app

if __name__ == "__main__":
    app.run()