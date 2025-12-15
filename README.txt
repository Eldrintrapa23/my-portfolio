
Simple Flask Portfolio App
--------------------------
Files created:
- app.py                : Flask application
- templates/index.html  : Public portfolio page
- templates/admin.html  : Admin page to add/delete projects
- static/style.css      : Styling
- static/profile.jpg    : Placeholder profile image
- static/project-placeholder.jpg : Placeholder project image
- portfolio.db          : SQLite database with sample projects

To run locally:
1. Ensure Python 3.8+ is installed.
2. Install dependencies:
     pip install flask pillow
3. From the portfolio_app directory run:
     python app.py
4. Open http://127.0.0.1:5000 in your browser.

The admin page is available at /admin (no auth in this simple example).
