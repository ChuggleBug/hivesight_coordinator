IMAGE_NAME=hvcoord_image
CONTAINER_NAME=hvcood_container

MOSQUITTO_HOST_PORT=1883

run: clean image
	docker run --privileged -d --name $(CONTAINER_NAME) \
	  	-v ./frontend:/workspace/frontend \
  		-v ./backend:/workspace/backend \
		-p $(MOSQUITTO_HOST_PORT):1883 \
		$(IMAGE_NAME)
	docker exec -it $(CONTAINER_NAME) /bin/bash

image: clean
	docker build -t $(IMAGE_NAME) .

clean:
	-@docker kill $(CONTAINER_NAME) 2>/dev/null || true
	-@docker rm -f $(CONTAINER_NAME) 2>/dev/null || true
	-@docker rmi -f $(IMAGE_NAME) 2>/dev/null || true

