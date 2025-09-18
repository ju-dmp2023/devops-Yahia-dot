# Use an official Nginx image as the base image
FROM nginx:alpine

# Set the working directory
WORKDIR /usr/share/nginx/html

# Copy the current directory contents into the container at /usr/share/nginx/html
COPY . .

# Copy the Nginx configuration template into the container
COPY nginx.conf.template /etc/nginx/nginx.conf.template

# Set the remote server address and Nginx port as environment variables with default values
ARG REMOTE_SERVER_ADDRESS=http://localhost:5001
ARG WEB_SERVER_ADDRESS=http://localhost:8080
ARG NGINX_PORT=8080
ENV REMOTE_SERVER_ADDRESS=${REMOTE_SERVER_ADDRESS}
ENV WEB_SERVER_ADDRESS=${WEB_SERVER_ADDRESS}
ENV NGINX_PORT=${NGINX_PORT}

# Create a config.js file with the remote server address
RUN echo "window.config = { remoteServerAddress: 'http://localhost:5001', webServerAddress: 'http://localhost:8080' };" > /usr/share/nginx/html/config.js

# Replace the placeholders in the nginx configuration template with the actual environment variable values
RUN envsubst '${REMOTE_SERVER_ADDRESS} ${NGINX_PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Expose the port specified by the environment variable
EXPOSE ${NGINX_PORT}

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]



