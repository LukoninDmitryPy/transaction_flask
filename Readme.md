# Project: Transaction Management

## Information

This project is designed to manage transactions in a system. It allows creating, canceling, and viewing transactions, as well as managing users who can perform these transactions.

The project is built using a microservices architecture, with separate services for user management, transaction management, and administration. This allows for scalability and flexibility in the system.

The project uses a database to store information about users and transactions. The database is designed to be secure and efficient, with indexing and caching to improve performance.

## Used Technologies

* Flask for creating a web application
* SQLAlchemy for working with a database
* Flask-Login for user authentication
* Flask-WTF for working with forms
* Flask-Blueprint for organizing the application into modules
* Alembic for database migrations
* Jinja2 for templating

## Endpoints

### User Endpoints

* `POST /api/register`: Register a new user
* `POST /api/login`: Login an existing user
* `POST /api/logout`: Logout the current user
* `GET /api/users`: Get a list of all users

### Transaction Endpoints

* `POST /api/create_transaction`: Create a new transaction
* `GET /api/transactions`: Get a list of all transactions
* `GET /api/transactions/<int:transaction_id>`: Get a specific transaction by ID
* `POST /api/transactions/<int:transaction_id>`: Cancel a specific transaction by ID

### Admin Endpoints

* `GET /api/admin/dashboard`: Get the admin dashboard
* `GET /api/admin/users`: Get a list of all users
* `GET /api/admin/transactions`: Get a list of all transactions
* `GET /api/admin/transactions/<int:transaction_id>`: Get a specific transaction by ID
* `PUT /api/admin/transactions/<int:transaction_id>`: Update a specific transaction by ID

### Running the Project with Docker Compose and Applying Migrations

1. Make sure you have Docker and Docker Compose installed.
2. Navigate to the project's root directory.
3. Run the project using the command `docker-compose up -d`.
4. To apply migrations, run the command `docker-compose exec web alembic upgrade head`.
5. Re-run containers after migrations `docker-compose restart`.








