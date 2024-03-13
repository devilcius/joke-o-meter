# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0](https://github.com/devilcius/joke-o-meter/tree/v1.0.0) - 2024-03-13

### Added
- Initial release of the joke-o-meter web application.
- Backend API developed using Django, providing endpoints for joke evaluation, results generation, and joke-o-meter rankings.
- Frontend application developed with React.js, featuring a welcome page, a card swiper interface for joke evaluation, and a results page.
- Implementation of a dynamic result system that assigns a character to the user based on their joke evaluations.
- Deployment configuration for serving the application using Nginx and Gunicorn.
- Content Security Policy (CSP) setup to enhance application security.
- Swagger documentation for the API endpoints.

### Fixed
- Addressed initial setup issues for serving static files and media through Nginx.
- Resolved CSP blocking issues related to the eval function and inline scripts.
