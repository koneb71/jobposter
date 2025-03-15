# JobPoster - Job Listing Application

A simple job listing application built with Django and Bootstrap, featuring an Airbnb-inspired design. This application allows employers to post job listings and job seekers to submit applications with resume uploads.

## Features

- **Job Listings**: Create, view, update, and delete job listings
- **Job Applications**: Submit applications for jobs with resume uploads
- **Search Functionality**: Search for jobs by title, company, location, or description
- **Responsive Design**: Mobile-friendly interface with Bootstrap
- **User Authentication**: Login and logout functionality for employers

## Technologies Used

- **Backend**: Django 5.1.7
- **Frontend**: Bootstrap 5, Font Awesome
- **Form Styling**: django-crispy-forms with crispy-bootstrap5
- **File Handling**: Pillow for image processing

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/jobposter.git
   cd jobposter
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Usage

### For Employers

1. Log in to your account
2. Click on "Post a Job" to create a new job listing
3. Fill in the job details and submit
4. View, edit, or delete your job listings

### For Job Seekers

1. Browse job listings on the home page
2. Use the search box to find specific jobs
3. Click on a job to view details
4. Click "Apply Now" to submit your application
5. Fill in your details, upload your resume, and submit

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [django-crispy-forms](https://django-crispy-forms.readthedocs.io/)

## Deployment

This project includes Docker configuration for easy deployment. Follow these steps to deploy:

### Prerequisites

- Docker and Docker Compose installed on your server
- A domain name (optional, but recommended for production)

### Deployment Steps

1. Clone the repository on your server:
   ```
   git clone https://github.com/yourusername/jobposter.git
   cd jobposter
   ```

2. Create a `.env` file based on the example:
   ```
   cp .env.example .env
   ```

3. Edit the `.env` file with your specific settings:
   ```
   # Generate a secure secret key
   SECRET_KEY=your-secure-secret-key
   
   # Set your domain name
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   
   # Set secure database credentials
   POSTGRES_PASSWORD=your-secure-password
   ```

4. Build and start the containers:
   ```
   docker-compose up -d
   ```

5. Create a superuser:
   ```
   docker-compose exec web python manage.py createsuperuser
   ```

6. Your application should now be running at http://yourdomain.com

### SSL/HTTPS Setup

For production, it's recommended to set up HTTPS. You can use Certbot with the Nginx container:

1. Install Certbot on your host machine
2. Obtain a certificate:
   ```
   certbot certonly --webroot -w ./nginx/certbot -d yourdomain.com -d www.yourdomain.com
   ```
3. Update the Nginx configuration to use the certificates
4. Restart the Nginx container:
   ```
   docker-compose restart nginx
   ```

### Maintenance

- To update the application:
  ```
  git pull
  docker-compose build web
  docker-compose up -d
  ```

- To view logs:
  ```
  docker-compose logs -f web
  ```

- To backup the database:
  ```
  docker-compose exec db pg_dump -U postgres jobposter > backup.sql
  ``` 