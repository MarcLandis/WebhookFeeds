<div markdown="1" style="max-width: 800px; margin: 0 auto;">

Webhook Feeds
=============

<p style="text-align:left;">
  <a href="https://github.com/marclandis/webhookfeeds">
    <img alt="Logo" src=".assets/logo.png" width="150px" />
  </a>
</p>

<p>
  <a href="https://github.com/marclandis/webhookfeeds/releases/latest"><img src="https://img.shields.io/github/release/marclandis/webhookfeeds.svg?style=flat-square" alt="GitHub release"></a>
  <a href="https://github.com/marclandis/webhookfeeds/actions?workflow=test"><img src="https://img.shields.io/github/actions/workflow/status/marclandis/webhookfeeds/test.yml?branch=main&label=test&logo=github&style=flat-square" alt="Test Status"></a>
  <a href="https://github.com/marclandis/webhookfeeds/actions?workflow=create-docker-image"><img src="https://img.shields.io/github/actions/workflow/status/marclandis/webhookfeeds/create-docker-image.yml?branch=main&label=build&logo=github&style=flat-square" alt="Build Status"></a>
  <a href="https://hub.docker.com/r/marclandis/webhookfeeds/"><img src="https://img.shields.io/docker/stars/marclandis/webhookfeeds.svg?style=flat-square&logo=docker" alt="Docker Stars"></a>
  <a href="https://hub.docker.com/r/marclandis/webhookfeeds/"><img src="https://img.shields.io/docker/pulls/marclandis/webhookfeeds.svg?style=flat-square&logo=docker" alt="Docker Pulls"></a>
</p>


### About

**Webhook Feeds** is a simple RESTful API to create and get feeds. For example, you can build a feed based on notification from [Diun](https://crazymax.dev/diun/), which was the reason to start this project.

### Documentation

[OpenAPI Documentation](/docs) is available when running the application.

#### Docker Compose with SQLite database:
```
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

#### Docker Compose with PostgresSQL database:
```
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
```
POSTGRES_DB=webhookfeeds
POSTGRES_USER=webhookfeeds
POSTGRES_PASSWORD=Password1234!
```

### Contributing

Feel free to contribute by starring the project, raising issues or even open a pull request.

### License

MIT - See [LICENSE.md](./LICENSE.md) for more details.
</div>
