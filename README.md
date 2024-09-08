
# Portfolio Backend

The back-end for my portfolio project, built with **Django** and **Django REST Framework (DRF)**. This backend handles websocket connections and exposes a REST API to a [React front-end](https://github.com/PixelOmen/portfolio_site). It handles user authentication (OAuth2), data management, and real-time communication using WebSockets, all deployed on AWS via [Terraform](https://github.com/PixelOmen/portfolio_terraform).

## Features / Tech Stack
- **Django**: Handles the entire project's business logic, authentication, task/data routing.
- **Django REST Framework (DRF)**: A robust framework the RESTful API provided to the front-end.
- **OAuth2**: Manages secure user authentication and token-based session handling via `drf-social-oauth2`.
- **Celery**: Task queue for managing background jobs such as email notifications and scheduled tasks.
- **Redis**: Used as in-memory datastore for the Celery broker, throttling cache, and websocket/chat cache.
- **WebSockets**: Implements real-time features for the chatbot demo.
- **Docker**: Both the web server and background task workers are containerized and orchestrated via AWS ECS.
- **AWS S3**: Stores and serves user-uploaded images. S3 is integrated seemlessly with Django's file storage system.
- **AWS RDS (PostgreSQL)**: Relational database used for data persistence managed via AWS RDS.
- **AWS ECS**: Containers are deployed on AWS Elastic Container Service (ECS) with RDS for PostgreSQL.

## WebSocket Routing / API Endpoints
The back-end exposes WebSocket routes and API endpoints to only the AWS CloudFront distribution through an application load balancer. Some of the key WebSocket routes and API endpoints include:
- **/socialauth/**: Handles OAuth2 authentication and token management.
- **/ws/chat/**: WebSocket endpoint for real-time chat functionality using Redis as a message broker and cache.
- **/api/v1/user-posts/**: Manages CRUD operations for user-generated messages.
- **/api/v1/user-images/**: Manages CRUD operations for user-uploaded images and generates pre-signed URLs to S3 bucket.

## Continuous Integration / Continuous Deployment (CI/CD)
The backend is integrated with **GitHub Actions** for automated deployment to AWS ECS. The following steps are triggered on each push to the staging or production branches:

- **Test:** Automated tests using Django’s testing framework for API endpoints, business logic, and database interactions.
- **Build and Push:** The Django application is containerized and pushed to **AWS ECR**.
- **Migration:** Database migrations are ran against **AWS RDS** through a standalone ECS task.
- **Deployment:** ECS Tasks are re-deployed with the newest images.
- **Monitoring**: Application logs and metrics are collected and monitored via **AWS CloudWatch**.

## License
[MIT](https://choosealicense.com/licenses/mit/)
