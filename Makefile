ON_BACKEND_RUN=docker-compose run --rm kl-backend

dev:
	export KUBECONFIG=devops/okta-kube-config

reset_db:
	${ON_BACKEND_RUN} bash -c 'echo "DROP SCHEMA public cascade; CREATE SCHEMA public" | python manage.py dbshell'
	${ON_BACKEND_RUN} python manage.py migrate
	${ON_BACKEND_RUN} python manage.py dbseed

clean_env:
	docker-compose down --volumes --rmi all --remove-orphans

test:
	docker-compose run --rm kl-backend python manage.py test

makemigrations:
	${ON_BACKEND_RUN} python manage.py makemigrations

docker_to_prod:
	kubectl config set-context --current --namespace=kl-prod
	kubectl apply -f devops/k8s/kl_deploy_app.yml

pip_install:
	docker-compose run --no-deps --rm kl-backend pip install -r requirements.txt