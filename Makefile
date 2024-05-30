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