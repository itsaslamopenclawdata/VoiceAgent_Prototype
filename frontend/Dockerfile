FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source
COPY . .

# Build for production
RUN npm run build

# Install serve for production
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Use serve for production or npm run dev for development
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
