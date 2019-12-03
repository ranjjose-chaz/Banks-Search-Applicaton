from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    path("db/", hello.views.db, name="db"),
    path("banks-html/", hello.views.banks_html, name="banks_html"),
    path("admin/", admin.site.urls),
    path('branches-html/', hello.views.bank_details_html, name="bank_details_html"),
    path('branches-html/<ifsc>/', hello.views.bank_details_html, name="bank_details_html"),
    path('branches2-html/', hello.views.branches2_html, name="branches2_html"),


    path("banks/<ifsc>/", hello.views.banks, name="banks"),
    path("branches/", hello.views.branches, name="branches"),

]
