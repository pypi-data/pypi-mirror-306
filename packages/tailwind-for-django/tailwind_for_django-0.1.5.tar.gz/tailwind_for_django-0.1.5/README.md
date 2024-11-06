# How to setup the library

This guide will take you through the steps to integrate Tailwind CSS into your Django project, including the necessary configurations, installing dependencies, and compiling CSS files. In the end, you will have a development-ready system with Tailwind CSS integrated.

 **Before starting, make sure you are in the main project folder**
## Step 1

Paste the following code in your terminal to download the library in your project.
Windows:
```bash
pip  install  tailwind_for_django
```
Mac:
```bash
pip3  install  tailwind_for_django
```
## Step 2 

In your settings.py the following line in the INSTALLED_APPS array.
```bash
'tailwind_for_django'
```

## Step 3

Now run the following command:

If you are in window:
```bash
python manage.py setup_tailwind
```
If you are in mac:
```bash
python3 manage.py setup_tailwind
```

## Step 4

Update your settings.py with this 2 line of code:
```bash
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

## Step 5 
Enter in static -> css -> input_tailwind.css and **remove the example line (the line start with //)**

## Step 6
Run the following script:
```bash
tailwind npm run build-css
```

## Step 7
In your templates insert the following code:
```bash
{% load static %}
<link  href="{% static 'output_tailwind.css' %}"  rel="stylesheet">
```
If you have some cache problem and your template style not update pass at your view **time** and change to the following code
```bash
{% load static %}
<link  href="{% static 'output_tailwind.css' %}?v={{  time.time  }}"  rel="stylesheet">
```

## Final 

Now you have tailwindcss installed on your django project.