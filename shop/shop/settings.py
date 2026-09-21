from pathlib import Path
import os
from decouple import config
import cloudinary

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
).split(',')

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
EXTERNAL_APPS =[
    'cloudinary',
  'cloudinary_storage',
  'django_ckeditor_5',
    'main',
    'accounts',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'social_django',
    'cart'
]

INSTALLED_APPS.extend(EXTERNAL_APPS)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

LOGIN_URL="log_in"
LOGIN_REDIRECT_URL ="index"
LOGOUT_URL="log_out"
LOGOUT_REDIRECT_URL ="log_in"

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]
SOCIAL_AUTH_PIPELINE = [
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',

    'accounts.pipeline.associate_by_email',

    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
]

# google oauth
SOCIAL_AUTH_URL_NAMESPACE = config('SOCIAL_AUTH_URL_NAMESPACE')
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

ROOT_URLCONF = 'shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processor.cart_total_amount',
            ],
        },
    },
]

CART_SESSION_ID = 'cart'
WSGI_APPLICATION = 'shop.wsgi.application'

# customizing auth
AUTH_USER_MODEL='accounts.CustomUser'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/kathmandu'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'static')
]
STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')
MEDIA_ROOT=os.path.join('media')
MEDIA_URL='/media/'

# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
#cloudinary
CLOUDINARY_STORAGE = {
'CLOUD_NAME': config('cloud_name'),
'API_KEY': config('api_key'),
'API_SECRET': config('api_secret'),
'SECURE': config('secure')
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

cloudinary.config(
cloud_name=config('cloud_name'),
api_key=config('api_key'),
api_secret=config('api_secret'),
secure=config('secure')
)

DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024


#ck editor 5
customColorPalette = [
        {
            'color': 'hsl(4, 90%, 58%)',
            'label': 'Red'
        },
        {
            'color': 'hsl(340, 82%, 52%)',
            'label': 'Pink'
        },
        {
            'color': 'hsl(291, 64%, 42%)',
            'label': 'Purple'
        },
        {
            'color': 'hsl(262, 52%, 47%)',
            'label': 'Deep Purple'
        },
        {
            'color': 'hsl(231, 48%, 48%)',
            'label': 'Indigo'
        },
        {
            'color': 'hsl(207, 90%, 54%)',
            'label': 'Blue'
        },
    ]

# CKEditor 5
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': {
            'items': [
                'heading', '|',
                'bold', 'italic', 'link',
                'bulletedList', 'numberedList',
                'blockQuote', 'imageUpload',
            ],
        },
    },

    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],

        'toolbar': {
            'items': [
                'heading', '|',
                'outdent', 'indent', '|',
                'bold', 'italic', 'link', 'underline',
                'strikethrough', 'code',
                'subscript', 'superscript', 'highlight', '|',
                'codeBlock', 'sourceEditing', 'insertImage',
                'bulletedList', 'numberedList', 'todoList', '|',
                'blockQuote', 'imageUpload', '|',
                'fontSize', 'fontFamily', 'fontColor',
                'fontBackgroundColor', 'mediaEmbed',
                'removeFormat', 'insertTable',
            ],
            'shouldNotGroupWhenFull': True,
        },

        'image': {
            'toolbar': [
                'imageTextAlternative', '|',
                'imageStyle:alignLeft',
                'imageStyle:alignRight',
                'imageStyle:alignCenter',
                'imageStyle:side', '|',
            ],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ],
        },

        'table': {
            'contentToolbar': [
                'tableColumn',
                'tableRow',
                'mergeTableCells',
                'tableProperties',
                'tableCellProperties',
            ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette,
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette,
            },
        },

        'heading': {
            'options': [
                {
                    'model': 'paragraph',
                    'title': 'Paragraph',
                    'class': 'ck-heading_paragraph',
                },
                {
                    'model': 'heading1',
                    'view': 'h1',
                    'title': 'Heading 1',
                    'class': 'ck-heading_heading1',
                },
                {
                    'model': 'heading2',
                    'view': 'h2',
                    'title': 'Heading 2',
                    'class': 'ck-heading_heading2',
                },
                {
                    'model': 'heading3',
                    'view': 'h3',
                    'title': 'Heading 3',
                    'class': 'ck-heading_heading3',
                },
            ],
        },
    },

    'list': {
        'properties': {
            'styles': True,
            'startIndex': True,
            'reversed': True,
        },
    },
} 

JAZZMIN_SETTINGS = {

    "site_brand": "Sajilo Cart",

    "welcome_sign": "Welcome to E-Commerce Management Portal",

    # Search model
    "search_model": "main.Product",

    # Custom CSS
    "custom_css": "css/jazzmin_custom.css",
    "site_logo": "images/logo.png",

    # Custom icons
    "icons": {

        # Authentication
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",

        # Main app models
        "main.Contact": "fas fa-address-book",

        "main.OfferProduct": "fas fa-tags",

        "main.Category": "fas fa-list",

        "main.SubCategory": "fas fa-list-alt",

        "main.Product": "fas fa-box",

        "main.ImageProduct": "fas fa-images",
        "main.ProductVariant": "fas fa-box"
    },

      "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "https://github.com/sujanlama90", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "main.Product"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "main"},
    ],
    "copyright": "Sajilo Cart",


    # Enable Jazzmin UI builder
    "show_ui_builder": True,
}

