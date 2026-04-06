# 🧑‍💻 HabitTracker

A backend API built with Django REST Framework, containerized with Docker. It enables users to create habits and track their daily progress through a streak-based system.

## 📦 Tech Stack
- Django REST Framework
- PostgreSQL (via Docker)
- Docker Compose (multi-container setup)


## 🧠 Tech Highlights
- Built REST API for habit tracking with daily completion logic
- Implemented streak calculation system
- Designed API endpoints using DRF generic views
- Containerized application with Docker and PostgreSQL


## API Example

# List all habits
```
GET /habits/
```

# Create new habit
```
POST /habits/
```

# Get a certain habit with its streak
```
GET /habits/<int:id>/
```

# Update habit details
```
PATCH/PUT /habits/<int:id>/
```

# Delete habit
```
DELETE /habits/<int:id>/
```

# Get logs of a certain habit about its activity
```
GET /habits/<int:id>/logs/
```

# Complete or uncomplete a certain habit  
```
POST /habits/<int:id>/toggle/
```


## 📈 Overall Growth
Through this project, I developed a solid understanding of building RESTful APIs with Django REST Framework, including the use of generic views and serializers. I also set up a Dockerized environment with PostgreSQL, gaining practical experience in structuring and running backend services.


## 🚦Running the Project
1. Clone the repository to your local machine.
2. Run ```docker-compose -f app.yaml up```.



## 🧪 Testing

```python manage.py test .```

