setup-docker:
	 python3 -m venv env
	 env/bin/python3 -m pip install --upgrade pip
	 env/bin/pip3 install -r requirements.txt

setup:
	 python3 -m venv env
	 env/bin/python3 -m pip install --upgrade pip
	 env/bin/pip3 install -r requirements-test.txt

run_app:
	uvicorn app.main:app 

test-crud:
	pytest tests/test-crud.py


