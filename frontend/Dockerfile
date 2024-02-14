# Use a node base image with your specified version
FROM node:18.14.2-alpine

# Set the working directory in the container
WORKDIR /frontend

# Copy package.json and package-lock.json to the container
COPY frontend/package*.json ./


# Install dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY frontend/ ./

# Build the React application for production
RUN npm run build

# Expose the port that the React app will run on
EXPOSE 3000

# Define the command to run the React app in production
CMD ["npm", "start"]