from sqladmin import ModelView
from mysite.database.models import (
    Country,
    UserProfile,
    ServiceCategory,
    Service,
    TeamMember,
    Client,
    Project,
    ProjectImage,
    Review,
    ContactRequest,
    BlogPost,
    RefreshToken,
)


class CountryAdmin(ModelView, model=Country):
    name = "Country"
    name_plural = "Countries"
    icon = "fa-solid fa-globe"

    column_list = [Country.id, Country.country_name, Country.country_code]
    column_searchable_list = [Country.country_name]
    column_sortable_list = [Country.id, Country.country_name]


class UserProfileAdmin(ModelView, model=UserProfile):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-users"

    column_list = [
        UserProfile.id,
        UserProfile.username,
        UserProfile.email,
        UserProfile.first_name,
        UserProfile.last_name,
        UserProfile.phone_number,
        UserProfile.user_role,
        UserProfile.registered_date,
    ]
    column_searchable_list = [UserProfile.username, UserProfile.email]
    column_sortable_list = [UserProfile.id, UserProfile.username, UserProfile.registered_date]
    column_details_exclude_list = [UserProfile.password]
    form_excluded_columns = [UserProfile.password]


class ServiceCategoryAdmin(ModelView, model=ServiceCategory):
    name = "Service Category"
    name_plural = "Service Categories"
    icon = "fa-solid fa-layer-group"

    column_list = [ServiceCategory.id, ServiceCategory.name, ServiceCategory.icon]
    column_searchable_list = [ServiceCategory.name]
    column_sortable_list = [ServiceCategory.id, ServiceCategory.name]


class ServiceAdmin(ModelView, model=Service):
    name = "Service"
    name_plural = "Services"
    icon = "fa-solid fa-briefcase"

    column_list = [
        Service.id,
        Service.title,
        Service.category_id,
        Service.price,
        Service.is_featured,
    ]
    column_searchable_list = [Service.title]
    column_sortable_list = [Service.id, Service.title, Service.price, Service.is_featured]


class TeamMemberAdmin(ModelView, model=TeamMember):
    name = "Team Member"
    name_plural = "Team Members"
    icon = "fa-solid fa-people-group"

    column_list = [
        TeamMember.id,
        TeamMember.first_name,
        TeamMember.last_name,
        TeamMember.position,
        TeamMember.country_id,
        TeamMember.is_active,
    ]
    column_searchable_list = [TeamMember.first_name, TeamMember.last_name, TeamMember.position]
    column_sortable_list = [TeamMember.id, TeamMember.first_name, TeamMember.last_name, TeamMember.is_active]


class ClientAdmin(ModelView, model=Client):
    name = "Client"
    name_plural = "Clients"
    icon = "fa-solid fa-building"

    column_list = [
        Client.id,
        Client.company_name,
        Client.website,
        Client.country_id,
        Client.is_featured,
    ]
    column_searchable_list = [Client.company_name]
    column_sortable_list = [Client.id, Client.company_name, Client.is_featured]


class ProjectAdmin(ModelView, model=Project):
    name = "Project"
    name_plural = "Projects"
    icon = "fa-solid fa-diagram-project"

    column_list = [
        Project.id,
        Project.title,
        Project.service_id,
        Project.client_id,
        Project.status,
        Project.is_featured,
        Project.created_date,
    ]
    column_searchable_list = [Project.title]
    column_sortable_list = [Project.id, Project.title, Project.status, Project.is_featured, Project.created_date]


class ProjectImageAdmin(ModelView, model=ProjectImage):
    name = "Project Image"
    name_plural = "Project Images"
    icon = "fa-solid fa-images"

    column_list = [ProjectImage.id, ProjectImage.project_id, ProjectImage.image_url, ProjectImage.caption]
    column_sortable_list = [ProjectImage.id, ProjectImage.project_id]


class ReviewAdmin(ModelView, model=Review):
    name = "Review"
    name_plural = "Reviews"
    icon = "fa-solid fa-star"

    column_list = [
        Review.id,
        Review.client_id,
        Review.author_name,
        Review.rating,
        Review.is_published,
        Review.created_date,
    ]
    column_sortable_list = [Review.id, Review.rating, Review.is_published, Review.created_date]


class ContactRequestAdmin(ModelView, model=ContactRequest):
    name = "Contact Request"
    name_plural = "Contact Requests"
    icon = "fa-solid fa-envelope"

    column_list = [
        ContactRequest.id,
        ContactRequest.name,
        ContactRequest.email,
        ContactRequest.subject,
        ContactRequest.status,
        ContactRequest.created_date,
    ]
    column_searchable_list = [ContactRequest.name, ContactRequest.email, ContactRequest.subject]
    column_sortable_list = [ContactRequest.id, ContactRequest.status, ContactRequest.created_date]


class BlogPostAdmin(ModelView, model=BlogPost):
    name = "Blog Post"
    name_plural = "Blog Posts"
    icon = "fa-solid fa-newspaper"

    column_list = [
        BlogPost.id,
        BlogPost.title,
        BlogPost.slug,
        BlogPost.is_published,
        BlogPost.created_date,
    ]
    column_searchable_list = [BlogPost.title, BlogPost.slug]
    column_sortable_list = [BlogPost.id, BlogPost.title, BlogPost.is_published, BlogPost.created_date]


class RefreshTokenAdmin(ModelView, model=RefreshToken):
    name = "Refresh Token"
    name_plural = "Refresh Tokens"
    icon = "fa-solid fa-key"

    column_list = [RefreshToken.id, RefreshToken.user_id, RefreshToken.created_at]
    column_sortable_list = [RefreshToken.id, RefreshToken.created_at]
