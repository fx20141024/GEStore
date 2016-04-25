if [ -d "./migrations" ]; then
	rm -rf "./migrations"
fi
python model.py db init
python model.py db migrate
python model.py db upgrade

