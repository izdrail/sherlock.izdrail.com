#!/bin/sh
.PHONY: build dev down ssh publish
build:
	docker image rm -f izdrail/security.izdrail.com:latest && docker --debug build -t izdrail/security.izdrail.com:latest --no-cache --progress=plain . --build-arg CACHEBUST=$(date +%s) 
dev:
	docker-compose -f docker-compose.yml up  --remove-orphans
down:
	docker-compose down
ssh:
	docker exec -it security.izdrail.com /bin/bash
publish:
	docker push izdrail/security.izdrail.com:latest
