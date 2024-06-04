# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dgerwig- <dgerwig-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/04 19:15:22 by dgerwig-          #+#    #+#              #
#    Updated: 2024/06/04 19:15:22 by dgerwig-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

DOCKER_NAME = 42_api

all:

docker:
	@echo "🟡 Building Docker with PYTHON 3.10"
	@docker build -t $(DOCKER_NAME) .
	@docker run \
		-v /etc/localtime:/etc/localtime:ro \
		-v ./data:/app/data \
		-it $(DOCKER_NAME)

user:
	@python3 scripts/get_users_by_campus.py

filter: user
	@python3 scripts/get_users_by_campus.py

rank:
	@python3 scripts/get_ranking_42.py

req:
	@pip3 install -r requirements.txt

clean:

fclean: clean
	@echo -e '\n🟡 Cleaning up...\n'
	@find . -type d -name '__pycache__' -exec rm -rf {} +

re:	fclean all

phony: all docker rank req clean fclean re
