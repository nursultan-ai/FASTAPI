from fastapi import FastAPI
import uvicorn

from mysite.database.db import Base, engine
from mysite.database.models import *
from mysite.admin.setup import create_admin
from mysite.admin.views import (
    CountryAdmin,
    UserProfileAdmin,
    ServiceCategoryAdmin,
    ServiceAdmin,
    TeamMemberAdmin,
    ClientAdmin,
    ProjectAdmin,
    ProjectImageAdmin,
    ReviewAdmin,
    ContactRequestAdmin,
    BlogPostAdmin,
    RefreshTokenAdmin,
)

from mysite.api.auth import auth_router
from mysite.api.country import router as country_router
from mysite.api.user import router as user_router
from mysite.api.service import router as service_router, category_router
from mysite.api.team import router as team_router
from mysite.api.client import router as client_router
from mysite.api.project import router as project_router, image_router
from mysite.api.review import router as review_router
from mysite.api.contact import router as contact_router
from mysite.api.blog import router as blog_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Antools figma",
    description="UX/UI site",
    version="1.0.0",
)

admin = create_admin(app)


admin.add_view(ClientAdmin)
admin.add_view(ProjectAdmin)
admin.add_view(CountryAdmin)
admin.add_view(UserProfileAdmin)
admin.add_view(ServiceCategoryAdmin)
admin.add_view(ServiceAdmin)
admin.add_view(TeamMemberAdmin)
admin.add_view(ProjectImageAdmin)
admin.add_view(ReviewAdmin)
admin.add_view(ContactRequestAdmin)
admin.add_view(BlogPostAdmin)
admin.add_view(RefreshTokenAdmin)

app.include_router(auth_router)
app.include_router(country_router)
app.include_router(project_router)
app.include_router(user_router)
app.include_router(service_router)
app.include_router(category_router)
app.include_router(team_router)
app.include_router(client_router)
app.include_router(image_router)
app.include_router(review_router)
app.include_router(contact_router)
app.include_router(blog_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000)
