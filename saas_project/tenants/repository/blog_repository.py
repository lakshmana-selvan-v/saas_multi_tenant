from ..model.blogs import Blogs

class BlogRepository:

    @staticmethod
    def create_blog(data, tenant_id, user_id):
        blog = Blogs.objects.create(
            tenant_id=tenant_id,
            user_id=user_id,
            title=data['title'],
            content=data['content'],
        )
        return blog
    
    @staticmethod
    def list_blogs(user_id):
        blogs = Blogs.objects.filter(user_id=user_id)
        return blogs

    @staticmethod
    def tenant_blogs():
        blogs = Blogs.objects.all()
        return blogs