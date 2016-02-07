# picture-app
Written using django-1.9 and python3.5. I recommend also to use <code>virtualenv</code> when installing project.
### Installing
To install the project run the following commands:

    git clone https://github.com/andrey-larionov/picture-app.git
    cd picture-app
    virtualenv venv -p /path/to/python3
    source venv/bin/activate
    pip install -r requirements.txt
### Running the project
Run the next command in <code>manage.py</code> directory:

    python3 manage.py runserver
### Examples
After running server you can send requests to picture-app REST API (in other terminal window of course). To send any request (except </code>/users/</code>) needs to be authorized user. Authorization uses token created when user creating. Bellow you can see some examples of requests to picture-app API (using <code>httpie</code>).
#### Create a user (Register):

    http --follow POST http://localhost:8000/users/ username='johndoe' email='johndoe@gmail.com' password='qwerty'
#### Get auth token by username and password (to use in other requests):

    http --follow POST http://localhost:8000/api-token-auth/ username='johndoe'  password='qwerty'
#### Upload a picture:

    http --form POST http://localhost:8000/pictures/ 'Authorization: Token <AUTH_TOKEN>' image@/path/to/image.png
#### Get list of pictures:
    
    http --follow GET http://localhost:8000/pictures/ 'Authorization: Token <AUTH_TOKEN>'
#### Get list of pictures belongs to specified user:

    http --follow GET http://localhost:8000/pictures/?u=<USER_ID> 'Authorization: Token <AUTH_TOKEN>'
#### Rate a picture:

    http --follow POST http://localhost:8000/pictures/rate/ 'Authorization: Token <AUTH_TOKEN>' picture=<PICTURE_ID> rate=9
#### Get list of pictures rated by authorized user:

    http --follow GET http://localhost:8000/pictures/rated/ 'Authorization: Token <AUTH_TOKEN>'
### Tests
To execute tests run the next command in <code>manage.py</code> directory:

    python3 manage.py test
