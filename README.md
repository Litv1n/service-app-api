# Pre-setup

#### After downloading go to the root directory of the project

```
cd service-app-api
```

# Build Docker containers

Build an app and database containers:

```
docker-compose build
```

# Usage

Run the docker containers:

```
docker-compose up
```

### User

#### Create a user

```
http://127.0.0.1:8000/api/user/create/
```

The app is using token authentication. After you register a user, you should get the token. Get the token via this ```url```:

```
http://127.0.0.1:8000/api/user/token/
```

Pass data for your user to get a personal token. Then you can use it through the app to access the API endpoints.

### Restaurant

#### List restaurants
```
http://127.0.0.1:8000/api/restaurant/restaurants/
```

#### Retrieve restaurant
Pass the ```id``` to get the restaurant instance. Example:

```
http://127.0.0.1:8000/api/restaurant/restaurants/2/
```

This ```url``` is for the restaurant instance with ```id=2```.

### Create, update and delete restaurant

This opportunities have only admin users. Use token for admin user to get the access.

#### Create restaurant

```
http://127.0.0.1:8000/api/restaurant/restaurants/
```

#### Update and delete restaurant

Pass the ```id``` for the ```url``` to get the opportunity to update and delete the restaurant instance

```
http://127.0.0.1:8000/api/restaurant/restaurants/38/
```

This ```url``` is for restaurant with ```id=38```.

### Menu

#### List of all menus

```
http://127.0.0.1:8000/api/menu/menus/
```

#### Menu detail

Pass the ```id``` to the url and get the menu instance with this ```id```.

```
http://127.0.0.1:8000/api/menu/menus/5/
```

### Create, update and delete menu

This opportunities have only admin users. Use token for admin user to get the access.

#### Create menu

```
http://127.0.0.1:8000/api/menu/menus/
```

#### Update and delete restaurant

Pass the ```id``` for the ```url``` to get the opportunity to update and delete the menu instance

```
http://127.0.0.1:8000/api/menu/menus/5/
```

This ```url``` is for menu with ```id=5```.

#### Current day menu:

General ```url```:

```
http://127.0.0.1:8000/api/menu/menus/?current-day-menu=menu_day
```

Where ```menu_day``` is a ```url``` parameter which means list all menus for a specific day. Example:

```
http://127.0.0.1:8000/api/menu/menus/?current-day-menu=W
```

This endpoint will list all menus for Wednesday.

Menu day choices:

```
M - Monday
T - Tuesday
W - Wednesday
TH - Thursday
F - Friday
S - Saturday
SU - Sunday
```

#### Vote 

Vote for the menu:

```
http://127.0.0.1:8000/api/menu/menus/vote
```

#### Top menu for the current day

Top menu by voting results for a certain day. General ```url```:

```
http://127.0.0.1:8000/api/menu/?top-menu=menu_day
```

Where ```menu_day``` is the day for which we want to see the best menu based on voting results. Example:

```
http://127.0.0.1:8000/api/menu/menus/?top-menu=S
```

This is the top menu for Saturday.

#### Upload image

```
http://127.0.0.1:8000/api/menu/menus/19/upload-image/
```

This ```url``` is for uploading image of menu for the menu with ```id=19```.

### Tests

To run all suites of tests:

```
docker-compose run --rm app sh -c "python manage.py test"
```

### API documentation

Schema swagger ui:

```
http://127.0.0.1:8000/docs/
```

Schema redoc:

```
http://127.0.0.1:8000/redoc/
```
