from django.contrib import admin

from .models import *

admin.site.register(MGame)
admin.site.register(MStatus)
admin.site.register(MCategory)
admin.site.register(MComment)
admin.site.register(MReply)
admin.site.register(MCommentReaction)
admin.site.register(MImage)
admin.site.register(MRating)

# Register your models here.
