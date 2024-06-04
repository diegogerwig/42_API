FROM python:3.10 

RUN apt update && apt install -y \
	bash \
	make 

WORKDIR /app/

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt \
	pip install --upgrade pip

CMD ["bash"]
# CMD ["bash", "-c", "make rank"]
