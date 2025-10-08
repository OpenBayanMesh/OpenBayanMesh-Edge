# OpenBayanMesh-Edge

Edge Node software for the OpenBayanMesh network infrastructure.

## Overview

OpenBayanMesh-Edge is a containerized edge node solution designed to facilitate distributed mesh networking. This software package enables edge devices to participate in the OpenBayanMesh ecosystem, providing decentralized connectivity and services.

## Features

- **Docker Compose Deployment**: Easy setup and management using Docker Compose orchestration
- **RESTful APIs**: Comprehensive API endpoints for node management and monitoring
- **Mesh Networking**: Seamless integration with the OpenBayanMesh network
- **Lightweight Architecture**: Optimized for edge computing environments
- **Scalable Design**: Support for multiple edge node deployments

## Requirements

- Docker Engine 20.10 or higher
- Docker Compose 2.0 or higher
- Linux-based operating system (recommended)
- Minimum 1GB RAM
- Network connectivity

## Installation

### Using Docker Compose

1. Clone the repository:
```bash
git clone https://github.com/OpenBayanMesh/OpenBayanMesh-Edge.git
cd OpenBayanMesh-Edge
```

2. Configure your environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the edge node:
```bash
docker-compose up -d
```

4. Verify the node is running:
```bash
docker-compose ps
```

## API Documentation

The Edge Node exposes several API endpoints for management and monitoring:

### Node Status
```
GET /api/status
```
Returns the current status of the edge node.

### Node Configuration
```
GET /api/config
POST /api/config
```
Retrieve or update node configuration.

### Network Information
```
GET /api/network
```
Provides information about mesh network connectivity.

### Health Check
```
GET /api/health
```
Health check endpoint for monitoring.

## Configuration

Configuration is managed through environment variables in the `.env` file:

- `NODE_ID`: Unique identifier for the edge node
- `MESH_NETWORK`: Network name to join
- `API_PORT`: Port for API access (default: 8080)
- `LOG_LEVEL`: Logging verbosity (debug, info, warn, error)

## Usage

### Starting the Node
```bash
docker-compose up -d
```

### Stopping the Node
```bash
docker-compose down
```

### Viewing Logs
```bash
docker-compose logs -f
```

### Restarting Services
```bash
docker-compose restart
```

## Development

For development and testing:

```bash
# Build local images
docker-compose build

# Run in development mode
docker-compose -f docker-compose.dev.yml up
```

## Troubleshooting

### Port Conflicts
If port 8080 is already in use, modify the `API_PORT` in your `.env` file.

### Connection Issues
Check network connectivity and firewall settings. Ensure required ports are open.

### Container Failures
Review logs with `docker-compose logs` for detailed error messages.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is dedicated to the public domain under CC0 1.0 Universal. See [LICENSE.md](LICENSE.md) for details.

## Support

For questions and support:
- Open an issue on GitHub
- Join the OpenBayanMesh community discussions

## Related Projects

- [OpenBayanMesh Core](https://github.com/OpenBayanMesh)
- OpenBayanMesh Cloud
- OpenBayanMesh Gateway
