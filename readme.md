

Build Docker image using the command 
`docker build -t shelldatathon .` and run it using the command `docker run -p 8000:5000 shelldatathon`


### Project structure
```
/myapp
    Dockerfile
    requirements.txt
    /app
        app.py
        /static
            /css
                style.css
            /js
                script.js
            /images
                logo.png
        /templates
            base.html
            login.html
            upload.html
            results.html
        /uploads
        /models
            model.pkl
        /modules
            data_processing.py
            model.py
```
