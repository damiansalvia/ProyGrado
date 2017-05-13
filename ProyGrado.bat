:: Levantar command-line
:: docker-machine restart default
docker-machine env default
docker start proyecto_contenedor /bin/bash || docker run -d -t -i -v /c/Github/ProyGrado:/ProyGrado/ --name proyecto_contenedor proyecto_image /bin/bash
docker exec -it proyecto_contenedor bash