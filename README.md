# Project Title: Open-Source FastAPI Celery Email Service

This project is an open-source email service built with Celery, RabbitMQ, and Redis. It's designed to be easy to use and highly scalable. We welcome contributions from anyone interested in improving the service.

### Prerequisites

You need to have the following installed on your machine:

- Docker
- Docker Compose

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-repo-url.git
```

2. Navigate to the project directory:

```bash
cd your-project-directory
```



### Setting up the Environment Variables

Before starting the service, you need to set up the environment variables that the application needs. These variables are stored in a `.env` file.

1. Create a `.env` file in the root directory of the project:

```bash
touch .env
```

2. Open the `.env` file and add the environment variables:

```bash
nano .env
```

The `.env` file should look something like this:

```env
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
CELERY_RESULT_BACKEND=redis://localhost:6379/0
EMAIL_HOST=your-email-host
EMAIL_PORT=your-email-port
EMAIL_HOST_USER=your-email-user
EMAIL_HOST_PASSWORD=your-email-password
```

Replace `your-email-host`, `your-email-port`, `your-email-user`, and `your-email-password` with your actual email service provider's SMTP server details.

3. Save and close the file.

Now, you can start the service as described in the Installation section. The application will automatically use the environment variables from the `.env` file.

### Start the service:

You can start the service by running the `start.sh` script:

```bash
./start.sh
```

Or you can use Docker Compose:

```bash
docker-compose up -d
```

## Contributing

We welcome contributions from anyone. If you're interested in contributing to this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Thanks to all the contributors who invest their time and effort to make this project better.
- Any other acknowledgments, inspirations, and resources used for this project.

Please replace `your-repo-url` and `your-project-directory` with your actual repository URL and project directory.