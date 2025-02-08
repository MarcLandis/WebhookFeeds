# Deployment

Webhook Feeds is deployed using Docker. You can use the build in SQLite database engine or any engines that is supported
by [SQLAlchemy](https://www.sqlalchemy.org)

Currently, there is no security implemented, so it is recommended to run this behind a reverse proxy with SSL enabled and some sort of authentication provided by the reverse proxy.

### Example docker-compose.yml

!!! note "SQLite"

    ``` yaml
    services:
      webhookfeeds:
        image: marclandis/webhookfeeds:latest
        container_name: webhookfeeds
        volumes:
          - database:/usr/src/app/database # SQLite database location
          - templates_custom:/usr/src/app/templates/custom # Custom templates location
        ports:
          - 8000:80
        restart: unless-stopped
    
    volumes:
      database:
      templates_custom:
    ```

!!! note "PostgreSQL"

    ``` yaml
    services:
      webhookfeeds:
        image: marclandis/webhookfeeds:latest
        container_name: webhookfeeds
        environment:
          - DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
        volumes:
          - templates_custom:/usr/src/app/templates/custom # Custom templates location
        ports:
          - 8000:80
        restart: unless-stopped
        
      postgres:
        image: postgres:17.2
        hostname: postgres
        container_name: postgres
        restart: unless-stopped
        volumes:
          - postgres_data:/var/lib/postgresql/data
        environment:
          POSTGRES_DB: ${POSTGRES_DB}
          POSTGRES_USER: ${POSTGRES_USER}
          POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
          
    volumes:
      postgres_data:
      templates_custom:
    ```

    .env file:
    
    ``` dotenv 
    POSTGRES_DB=webhookfeeds
    POSTGRES_USER=webhookfeeds
    POSTGRES_PASSWORD=Password1234!
    ```
