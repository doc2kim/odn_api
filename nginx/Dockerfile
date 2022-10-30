FROM nginx:latest

# Configure Nginx
COPY nginx.conf /etc/nginx/nginx.conf


# Copy Script to Wait for Gunicorn
COPY wait-for-it.sh /wait-for-it.sh

# Copy Entrypoint Script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
