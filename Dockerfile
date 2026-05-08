# Usa uma imagem oficial do Python.
FROM python:3.9.6-slim

# Impede que o Python grave arquivos .pyc e força o log a aparecer no terminal.
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

# Instala as dependências.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o projeto para dentro do container.
COPY . .

# Coleta os arquivos estáticos (CSS, JS, Imagens).
RUN python manage.py collectstatic --noinput

# Inicia o servidor com Gunicorn. O número de workers e threads pode ser ajustado conforme necessário.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 emh.wsgi:application