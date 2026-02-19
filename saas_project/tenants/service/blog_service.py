from ..repository.blog_repository import BlogRepository



class BlogService:


    @staticmethod
    def create_blog(data, tenant_id, user_id):
        blog = BlogRepository.create_blog(data, tenant_id, user_id)
        return blog

    @staticmethod
    def list_blogs(user_id):
        blogs = BlogRepository.list_blogs(user_id)
        return blogs

    @staticmethod
    def tenant_blogs():
        blogs = BlogRepository.tenant_blogs()
        blogs_data = []
        for blog in blogs:
            blogs_data.append({
                "id": blog.id,
                "title": blog.title,
                "content": blog.content,
            })
        return blogs_data