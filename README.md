# movie-system
A simple HTTP server with flask for IE course at university

## Features
- Multiple HTTP endpoints
- Proper HTTP methods usage
- Return related responses

## Get Started
```bash
# Clone this repository to your machine
git clone https://github.com/MrezaDorudian/movie-system.git

# Navigate to the downloaded folder
cd movie-system
```

## Installation
```bash
# Build container
docker build --tag movie_app .

# Run the container
docker run -d -p 8080:8080 movie_app
```
