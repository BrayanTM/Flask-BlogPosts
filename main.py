from blogapp import create_app

# Crear la aplicación Flask
app = create_app()

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
