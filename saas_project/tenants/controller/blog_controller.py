from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..service.blog_service import BlogService
from ..core.context_variable import get_current_tenant_id

@api_view(["POST"])
def create_blog(request, user_id):
    data = request.data
    tenant_id = get_current_tenant_id()
    blog = BlogService.create_blog(data, tenant_id, user_id)
    return Response(
        {"message": "Blog created successfully", "blog_id": blog.id},
        status=status.HTTP_201_CREATED,
    )

@api_view(["GET"])
def list_blogs(request, user_id):
    blogs = BlogService.list_blogs(user_id)
    blogs_data = []
    for blog in blogs:
        blogs_data.append({
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
        })
    return Response(
        {"message": "Blogs listed successfully", "blogs": blogs_data},
        status=status.HTTP_200_OK,
    )

@api_view(["GET"])
def tenant_blogs(request):
    blogs = BlogService.tenant_blogs()
    return Response(
        {"message": "Tenant blogs listed successfully", "blogs": blogs},
        status=status.HTTP_200_OK,
    )