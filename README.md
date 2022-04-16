# Dafiti API

> First, let's agree that since it's a technical test, I'm going to leave the .env credentials exposed in example.env. So let's move on =)

## Stories

> **ME** as admin user
> 
> **I WANT** to be able to manage **ALL** users
> 
> **ALL** the products
> 
> And **ALL** categories

> **ME** as a staff user
> 
> **I NEED** an admin user to register
> 
> **SO THAT** I can have access to the administration
> 
> of **ALL** products
> 
> and **ALL** categories

## First Steps

### Run localy

> Make sure you have created the .env file based on the example.env file

### With the `make` command (recommended)

Just run the following command:

```commandline
make setup
```

This command will make all the necessary configurations to manually upload and test the application. In addition, it creates a super user to access the /admin/ endpoint and the other endpoints with the following credentials:

```json
{
  "email": "dafiti@dafiti.com",
  "password": "dafiti"
}
```

To access the routes, take the token received when logging in and use it in the request header with the following pattern:

| Key           | Value           |
|---------------|-----------------|
| Authorization | Token < token > |

### Without the `make` command (not recommended)

1. 
```commandline
docker volume create --name=db_persist
```

2.
```commandline
docker-compose build --no-cache
```

3.
```commandline
docker-compose run web bash -c "python manage.py makemigrations && python manage.py migrate && python manage.py create_superuser && python manage.py create_products && python manage.py create_randomusers"
```

## Tests

To run the tests, just use the `make test` command (with make command)

or:
```commandline
docker-compose run web bash -c "coverage run ./manage.py test -v 3 && coverage report"
```
without `make` command.

> All `make` commands are in the `Makefile`. I strongly recommend using it to your advantage in development.

## Run

To launch the application with the `make` command, just run the following command:

```commandline
make run
```

Without the `make` command:

```commandline
docker-compose up
```

## API

`base_url` = http://localhost:8000/api/v1/

### Login

----

**Endpoint: `login/`**

Method: `POST`

Header: `No Header`

Status: `200 OK`

Body: 

```json
{
  "email": "doc@readme.md",
  "password": "readme"
}
```

Response Example:

```json
{
  "id": 203,
  "last_login": "2022-04-16T01:48:51.289333-03:00",
  "is_superuser": false,
  "is_staff": false,
  "email": "doc@readme.md",
  "name": "Doc",
  "document": "00011122233",
  "token": "8bba19c9fe4dc2c9d1c562303e4906d647a44ba1"
}
```

> Note: This token expires every 1 hour. But don't worry, it only expires after an hour if you log in. We don't want your session to fall in the middle of an important task =)

----

### User

----

**Endpoint: `user/`**

Method: `GET`

Accepted filtering parameters: `page`, `id`, `last_login`, `is_active`, `date_joined`, `email`, `name`, `document`

Header: `Authorization: Token <token>[is_superuser=true]`

Status: `200 OK`

Body: `No Body`

Response Example:

```json
{
  "count": 101,
  "next": "http://localhost:8000/api/v1/user/?page=2",
  "previous": null,
  "results": [
    {
      "id": 6,
      "last_login": null,
      "is_superuser": false,
      "is_staff": false,
      "email": "louisconway@example.com",
      "name": "Ariel",
      "document": "65625248737"
    },
    {
      "id": 16,
      "last_login": null,
      "is_superuser": false,
      "is_staff": false,
      "email": "bhoffman@example.net",
      "name": "Mark",
      "document": "24550560665"
    },
    {
      "id": 58,
      "last_login": null,
      "is_superuser": false,
      "is_staff": false,
      "email": "wkelly@example.org",
      "name": "Charles",
      "document": "27762125779"
    },
    ...
    // Default: 15 per page  
  ]
}
```

----

**Endpoint: `user/<int:user_id>/`**

Method: `GET`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `200 OK`

Body: `No Body`

Response Example:

```json
{
  "id": 16,
  "last_login": null,
  "is_superuser": false,
  "is_staff": false,
  "email": "bhoffman@example.net",
  "name": "Mark",
  "document": "24550560665"
}
```

> Note: If you are not a superuser, you can only **get retrieve**, and only on yourself.

----

**Endpoint: `user/`**

Method: `POST`

Header: `Authorization: Token <token>[is_superuser=true]`

Status: `201 CREATED`

Body: 

```json
{
  "name": "Doc",
  "document": "00011122233",
  "email": "doc@readme.md",
  "password": "readme"
}
```

Response example:

```json
{
  "id": 203,
  "last_login": null,
  "is_superuser": false,
  "is_staff": false,
  "email": "doc@readme.md",
  "name": "Doc",
  "document": "00011122233",
  "token": "1db5d82e55ef0685ac674464d8939cc05c45ab8d"
}
```

----

**Endpoint: `user/<int:user_id>/`**

Method: `PATCH`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `200 OK`

Body: 
```json
{
  "name": "Docker"
}
```

```json
{
  "id": 203,
  "last_login": "2022-04-16T00:39:08.344401-03:00",
  "is_superuser": false,
  "is_staff": false,
  "email": "doc@readme.md",
  "name": "Docker",
  "document": "00011122233"
}
```

> Note: If you are not a superuser, you can only **patch yourself**.
 
----

**Endpoint: `user/<int:user_id>/`**

Method: `DELETE`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `204 NO CONTENT`

Body: `No Body`

Response Example: `No Content`

> Note: If you are not a superuser, you can only **delete yourself**.

----

### Product

**Endpoint: `product/`**

Method: `GET`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Accepted filtering parameters: `page`, `id`, `is_active`, `date_joined`, `date_joined`, `title`, `description`, `price`, `stock`

Status: `200 OK`

Body: `No Body`

Response Example:

```json
{
  "count": 403,
  "next": "http://localhost:8000/api/v1/product/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "date_joined": "2022-04-15T21:04:29.467268-03:00",
      "date_modified": "2022-04-15T21:32:31.217941-03:00",
      "is_active": true,
      "title": "Red Pants",
      "description": "List shake stand capital effort name television where. Travel answer parent all. Trial family see wish.",
      "image": null,
      "price": 141.0,
      "stock": 70.0,
      "categories": [
        {
          "id": 3,
          "name": "Vintage"
        }
      ]
    },
    {
      "id": 2,
      "date_joined": "2022-04-15T21:05:02.236048-03:00",
      "date_modified": "2022-04-15T21:05:02.236074-03:00",
      "is_active": true,
      "title": "Black Shirt",
      "description": "Popular particular over another section maintain court special. Choice amount hold loss.\nBaby someone run person. Behind miss available sea whether move arrive difference.",
      "image": null,
      "price": 162.0,
      "stock": 10.0,
      "categories": []
    },
    ... // Default: 15 per page
  ]
}
```

----
 
**Endpoint: `product/<int:product_id>/`**

Method: `GET`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `200 OK`

Body: `No Body`

Response Example:
```json
{
  "id": 1,
  "date_joined": "2022-04-15T21:04:29.467268-03:00",
  "date_modified": "2022-04-15T21:32:31.217941-03:00",
  "is_active": true,
  "title": "Red Pants",
  "description": "List shake stand capital effort name television where. Travel answer parent all. Trial family see wish.",
  "image": null,
  "price": 141.0,
  "stock": 70.0,
  "categories": [
    {
      "id": 3,
      "name": "Vintage"
    }
  ]
}
```

----

**Endpoint: `product/`**

Method: `POST`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `201 CREATED`

Body:

```json
{
  "title": "Yellow Short",
  "description": "bla",
  "price": 145,
  "stock": 14,
  "categories": [
    {
      "name": "Summer"
    },
    {
      "name": "Ice"
    }
  ]
}
```

Response Example:

```json
{
  "id": 1335,
  "title": "Yellow Short",
  "description": "bla",
  "image": null,
  "price": 145.0,
  "stock": 14,
  "date_joined": "2022-04-16T06:40:43.856187-03:00",
  "date_modified": "2022-04-16T06:40:43.856205-03:00",
  "is_active": true,
  "categories": [
    {
      "id": 4,
      "name": "Summer"
    },
    {
      "id": 6,
      "name": "Ice"
    }
  ]
}
```

----

**Endpoint: `product/<int:product_id>/`**

Method: `PATCH`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `200 OK`

Body:

```json
{
  "title": "Blue Shirt",
  "categories": [
    {
      "name": "Ice"
    }
  ]
}
```

Response Example:
```json
{
  "id": 100,
  "title": "Blue Shirt",
  "description": "Begin American success fight.\nCould four pick keep live young us necessary. Under claim now dinner effect force. Before reality require prepare discuss turn south course.",
  "image": null,
  "price": 154.0,
  "stock": 99.0,
  "date_joined": "2022-04-15T21:05:49.049617-03:00",
  "date_modified": "2022-04-15T21:05:49.049651-03:00",
  "is_active": true,
  "categories": [
    {
      "id": 6,
      "name": "Ice"
    }
  ]
}
```

----

**Endpoint: `product/<int:product_id>/`**

Method: `DELETE`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `204 NO CONTENT`

Body: `No Body`

Response Example: `No Content`

>

**Endpoint: `product/export/csv/`**

Method: `GET`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `200 OK`

Body: `No Body`

Response Example: `ProductsModel.csv`

----

**Endpoint: `product/import/csv/`**

Method: `POST`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `200 OK`

Body:
```json
{
  "file": "InMemoryUploadedFile.csv"
}
```

| Product ID                | Title    | Description | Image    | Price           | Stock         | Categories                                                           | Date Joined           | Date Modified         | Is Active              |
|---------------------------|----------|-------------|----------|-----------------|---------------|----------------------------------|-----------------------|-----------------------|------------------------|
| Leave blank to create     | Required | Required    | Optional | Required(float) | Required(int) | Optional(Many to Many Field. Separator: " \ ", example: "6 \ 1 \ 4") | Optional(default=now) | Optional(default=now) | Optional(default=True) |

> Note: You can import and export files from the admin panel as well.

Response Example:
```json
{
  "count_lines": 448,
  "count_errors": 0,
  "errors": []
}
```

----

### Category

----
 
**Endpoint: `category/`**

Method: `GET`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Accepted filtering parameters: `page`, `id`, `is_active`, `date_joined`, `date_modified`, `name`

Status: `200 OK`

Body: `No Body`

Response Example:
```json
{
  "count": 9,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Kids"
    },
    {
      "id": 2,
      "name": "Classic"
    },
    {
      "id": 3,
      "name": "Vintage"
    },
    ... // Default: 15 per page
  ]
}
```

----

**Endpoint: `category/<int:category_id>/`**

Method: `GET`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `200 OK`

Body: `No Body`

Response Example:

```json
{
  "id": 1,
  "name": "Kids"
}
```

----
 
**Endpoint: `category/`**

Method: `POST`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `201 CREATED`

Body:

```json
{
  "name": "Old School"
}
```

Response Example:
```json
{
  "id": 10,
  "name": "Old School"
}
```

----
 
**Endpoint: `category/<int:category_id>/`**

Method: `PATCH`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `200 OK`

Body:
```json
{
  "name": "Doc"
}
```

Response Example:
```json
{
  "id": 10,
  "name": "Doc"
}
```

> Note: You cannot edit a category for a category name that already exists.

----

**Endpoint: `category/<int:category_id>/`**

Method: `DELETE`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `204 NO CONTENT`

Body: `No Body`

Response Example: `No Content`
