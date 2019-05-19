
docker:
	docker build -t user_hierarchy:1.0.0 . && docker run -ti user_hierarchy:1.0.0

main:
	python3 src/user_hierarchy/main.py --users resources/users.json --roles resources/roles.json

more:
	python3 src/user_hierarchy/main.py --users resources/users-more.json --roles resources/roles-more.json

tests:
	python3 src/user_hierarchy/tests.py
