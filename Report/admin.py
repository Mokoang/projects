# from django.contrib import admin
# from .models import lease_report
# from django.contrib import admin
# from django.template.response import TemplateResponse
# from django.urls import path,include


# @admin.register(lease_report)
# class SecurityAdmin(admin.ModelAdmin):

#     def get_urls(self):

#         # get the default urls
#         urls = super(SecurityAdmin, self).get_urls()

#         # define security urls
#         security_urls = [
#             path('', self.admin_site.admin_view(self.security_configuration))
#             # Add here more urls if you want following same logic
#         ]

#         # Make sure here you place your added urls first than the admin default urls
#         return security_urls + urls

#     # Your view definition fn
#     def security_configuration(self, request):
#         context = dict(
#             self.admin_site.each_context(request), # Include common variables for rendering the admin template.
#             something="test",
#         )
#         return TemplateResponse(request, "report.html", context)
