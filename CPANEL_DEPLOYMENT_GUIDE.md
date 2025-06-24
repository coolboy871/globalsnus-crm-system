# cPanel Deployment Guide for Global Snus CRM

## Database Setup Complete ✅
- Database Name: `globalsnuscrm`
- Database User: `globalsnuscrm_admin`
- Database Password: `global1111snus+7555asad`
- Configuration updated in `settings_production.py`
- MySQL connector added to `requirements.txt`

## Next Steps for cPanel Deployment

### 1. Upload Files to cPanel
1. Compress your project folder into a ZIP file
2. Upload to your cPanel File Manager in the `public_html` directory
3. Extract the files

### 2. Install Python Packages
In cPanel Terminal or SSH, navigate to your project directory and run:
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables (Recommended for Security)
In cPanel, set these environment variables:
- `DJANGO_SETTINGS_MODULE=globalsnus_crm.settings_production`
- `DB_NAME=globalsnuscrm`
- `DB_USER=globalsnuscrm_admin`
- `DB_PASSWORD=global1111snus+7555asad`
- `DJANGO_SECRET_KEY=your-secure-secret-key-here`

### 4. Run Database Migrations
```bash
python manage.py migrate --settings=globalsnus_crm.settings_production
```

### 5. Create Superuser
```bash
python manage.py createsuperuser --settings=globalsnus_crm.settings_production
```

### 6. Collect Static Files
```bash
python manage.py collectstatic --settings=globalsnus_crm.settings_production
```

### 7. Configure WSGI Application
Make sure your `passenger_wsgi.py` file is configured correctly for cPanel.

### 8. Test the Application
- Access your domain to test the application
- Check the admin panel at `/admin`
- Verify database connectivity

## Troubleshooting

### Common Issues:
1. **MySQL Connection Error**: Verify database credentials in cPanel MySQL section
2. **Static Files Not Loading**: Check STATIC_ROOT and STATIC_URL settings
3. **Permission Errors**: Ensure proper file permissions (755 for directories, 644 for files)

### Log Files:
- Django errors will be logged to `django_errors.log` in your project root
- Check cPanel error logs for server-related issues

## Security Notes:
- The database password is currently in the settings file for simplicity
- For production, consider using environment variables for all sensitive data
- Update `ALLOWED_HOSTS` with your actual domain names
- Generate a new `SECRET_KEY` for production use

## File Structure After Deployment:
```
public_html/
├── globalsnus_crm/
├── factory/
├── static/
├── media/
├── templates/
├── manage.py
├── passenger_wsgi.py
├── requirements.txt
└── django_errors.log (created after first error)
