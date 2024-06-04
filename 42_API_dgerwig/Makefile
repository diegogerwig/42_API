all:

rank:
	@python3 ./scripts/get_ranking_42.py

req:
	@pip3 install -r requirements.txt

clean:

fclean: clean
	@echo -e '\n🟡 Cleaning up...\n'
	@find . -type d -name '__pycache__' -exec rm -rf {} +

re:	fclean all

phony: all req clean fclean re
