# run tests
test:
	cd app && pytest -n auto

# run task worker, we can spawn an infinite number of workers, generally 1 per CPU core
worker:
	cd app && celery -A scheduler worker -l INFO