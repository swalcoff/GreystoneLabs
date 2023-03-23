.PHONY: run clean install

run:
	uvicorn main:app --reload

clean:
	rm -f greystone.db

install:
	pip3 install -r requirements.txt
