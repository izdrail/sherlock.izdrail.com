.PHONY: build
build:
	docker build -t izdrail/security.izdrail.com .

.PHONY: run
run:
	docker run -p 8000:8000 -d izdrail/security.izdrail.com

.PHONY: stop
stop:
	docker stop security.izdrail.com

.PHONY: rm
rm:
	docker rm security.izdrail.com

.PHONY: dev
dev:
	npm run dev

.PHONY: publish
publish:
	docker push izdrail/security.izdrail.com:latest