FROM node:20-alpine

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source
COPY . .

# Remove node_modules and rebuild fresh in Docker
RUN rm -rf node_modules && npm install

# Expose port
EXPOSE 3000

# Run in development mode with hot reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
