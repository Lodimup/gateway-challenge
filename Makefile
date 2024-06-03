# run tests
test:
	cd app && pytest -n auto
# run task worker, we can spawn an infinite number of workers, generally 1 per CPU core
worker:
	cd app && celery -A scheduler worker -l INFO
# Tag & trigger github actions to build and push docker image
release:
	ver=$(shell date +%Y.%m.%d.%s) &&\
	echo $$ver &&\
	git tag -a $$ver -m "Release $$ver" &&\
	git push origin $$ver
# Make a requirements.txt file for deployment
requirements:
	poetry config warnings.export false
	poetry add poetry-plugin-export -G dev
	poetry export -f requirements.txt --output requirements.txt --without-hashes

# Build & run docker container
test-docker: test-build test-run
test-build:
	docker build -t gateway:latest .
test-run:
	docker run -p 8080:80 --env-file .env gateway:latest
# Run all services in docker-compose
compose-up:
	docker-compose up -d