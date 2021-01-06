#Ali: I comment because I don't need!
# pip3 install flask_sqlalchemy
# pip3 install flask_cors
# pip3 install flask --upgrade
# pip3 uninstall flask-socketio -y
# service postgresql start

#Ali: I changed the below from [su -] to [sudo -u] and changed the path to the files! This is the only way it worked!
sudo -u postgres bash -c "psql < /home/ali/fullstackdevelop/FSND/bookshelf/backend/setup.sql"
sudo -u postgres bash -c "psql bookshelf < /home/ali/fullstackdevelop/FSND/bookshelf/backend/books.psql"