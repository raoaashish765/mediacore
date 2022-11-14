from django.contrib import admin
from .models import *

admin.site.register(setting)
admin.site.register(Follow)
admin.site.register(Unfpenalty)
admin.site.register(Allposts)
admin.site.register(Postlikes)
admin.site.register(Postcomments)
admin.site.register(Repo)