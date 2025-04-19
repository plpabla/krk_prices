# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
# Copy package files first to leverage Docker cache
COPY package*.json ./
RUN npm ci --quiet

# Copy source code and build
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
# Copy built static files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html
# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# Use the following command to build the Docker image
# docker build -t frontend:latest .

# Use the following command to run the Docker container
# docker run -d -p 8080:80 frontend:latest