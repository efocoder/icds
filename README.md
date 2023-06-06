# ICD Codes API

This a simple API for recording and tracking ICD codes

## Architectural consideration

Utilized relationship between Categories and the Codes table. Each category is
referenced in the codes table.

Since the sample csv file for codes contains both category code and the category title, I removed the title and used the
code to fetch respective categories to be reference. The title can be accessed through quering related table

### To get this application running, follow these steps;

1. Clone the git repository
   ```bash
    git clone https://github.com/efocoder/icds.git
   ```
2. In order to run the application, you need to have Docker installed on your system.

   ## Run application

2.1 Build first.

  ```docker-compose
    docker-compose up
   ```

The above command will set up the code and add the categories into the db, also it
adds a test user to the system.

### Test Logins

```
username: testuser
Password: pas12345
```

## Endpoints

Login: `/auth/jwt/create/`

Categories: `/categories/`

Codes: `/codes/`

Upload CSV: `codes/upload_data`

API can be accessed through the Browsable API in your browser at `localhost:8000`
