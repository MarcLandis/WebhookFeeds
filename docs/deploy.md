# Deployment

Webhook Feeds is deployed using Docker. You can use the build in SQLite database engine or any engines that is supported by [SQLAlchemy](https://www.sqlalchemy.org)

### Example docker-compose.yml

!!! note "SQLite"
    ``` yaml
    services:
      webhookfeeds:
        image: marclandis/webhookfeeds:latest
        container_name: webhookfeeds
        volumes:
          - database:/usr/src/app/database # SQLite database location
        ports:
          - 8000:8000
        restart: unless-stopped
    
    volumes:
      database:
    ```

!!! note "PostgreSQL"
    ``` yaml
    services:
      webhookfeeds:
        image: marclandis/webhookfeeds:latest
        container_name: webhookfeeds
        environment:
          - DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
        ports:
          - 8000:8000
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
    ```

    .env file:
    
    ``` dotenv 
    POSTGRES_DB=webhookfeeds
    POSTGRES_USER=webhookfeeds
    POSTGRES_PASSWORD=Password1234!
    ```