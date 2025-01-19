FROM python:3.12.7

# Set working directory
WORKDIR /usr/src/app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron tzdata && rm -rf /var/lib/apt/lists/*

# Set timezone to Japan
ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Add crontab entry for running hoge.py at 6 AM
RUN echo "0 6 * * * /start.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/app-cron && \
    chmod 0644 /etc/cron.d/app-cron && \
    crontab /etc/cron.d/app-cron

# Create the startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Start both cron and the Flask app
CMD ["sh", "-c", "service cron start && flask run --host=0.0.0.0 --debug"]
