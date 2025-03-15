Flask CRUD API with JWT Authentication

Overview
This is a basic CRUD API built using Flask and MySQL, with JWT authentication for secure user management. The API supports operations for registering users, logging in, and performing CRUD operations on user data.e

FEATURES
✅ User Registration & Authentication(JWT-based login system)
✅ CRUD Operations (Create, Read, Update, Delete users)
✅ Secure Password Hashing (bcrypt)
✅ Modular Code structures for scability

Tech Stack
* Backend: Flask(Python)
* Database: MySQL
* Authentication: Flask-JWT-Extended(JsonWeb Token)
* Password Security: bcrypt
* Testing & Debugging: Postman

## API Endpoints Overview  

### Authentication  
| Method | Endpoint  | Description  |
|--------|----------|-------------|
| POST   | `/register` | Register a new user  |
| POST   | `/login`    | Login and get a JWT token |

### User Management  
| Method | Endpoint           | Description  |
|--------|--------------------|-------------|
| GET    | `/users`           | Get all users |
| GET    | `/users/<user_id>` | Get a single user by ID |
| PUT    | `/users/<user_id>` | Update user details |
| DELETE | `/users/<user_id>` | Delete a user |


