init:
	pip install -r requirements.txt --use-mirrors

test:
	nosetests tests

install:
	sudo python setup.py install
