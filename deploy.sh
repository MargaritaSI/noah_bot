#!/bin/bash

# Noah Lieven Bot - Deployment Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_error ".env file not found!"
    print_status "Please copy env.example to .env and configure your settings:"
    echo "cp env.example .env"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running!"
    exit 1
fi

# Parse command line arguments
MODE=${1:-dev}

case $MODE in
    dev)
        print_status "Starting development environment..."
        docker-compose -f docker-compose.dev.yml up --build
        ;;
    prod)
        print_status "Starting production environment..."
        docker-compose -f docker-compose.prod.yml up -d --build
        ;;
    stop)
        print_status "Stopping all services..."
        docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
        docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
        ;;
    logs)
        print_status "Showing logs..."
        docker-compose -f docker-compose.dev.yml logs -f 2>/dev/null || \
        docker-compose -f docker-compose.prod.yml logs -f
        ;;
    clean)
        print_status "Cleaning up Docker resources..."
        docker-compose -f docker-compose.dev.yml down -v 2>/dev/null || true
        docker-compose -f docker-compose.prod.yml down -v 2>/dev/null || true
        docker system prune -f
        ;;
    *)
        echo "Usage: $0 {dev|prod|stop|logs|clean}"
        echo ""
        echo "Commands:"
        echo "  dev   - Start development environment"
        echo "  prod  - Start production environment"
        echo "  stop  - Stop all services"
        echo "  logs  - Show logs"
        echo "  clean - Clean up Docker resources"
        exit 1
        ;;
esac
