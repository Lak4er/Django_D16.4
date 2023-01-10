# from django.db import models
# from django.db.models import Sum
# from django.contrib.auth.models import User
# # from datetime import datetime
#
#
# class Author(models.Model):
#     author_user = models.OneToOneField(User, on_delete=models.CASCADE)
#     author_rating = models.IntegerField(default=0, null=True)
#
#     def update_rating(self):
#         post_rating = self.post_set.aggregate(post_rating=Sum('post_rating'))
#
#         p_rat = 0
#         p_rat += post_rating.get('post_rating')
#
#         comment_rat = self.author_user.comment_set.aggregate(comment_rating=Sum('comment_rating'))
#         c_rat = 0
#         c_rat += comment_rat.get('comment_rating')
#
#         self.author_rating = p_rat * 3 + c_rat
#         self.save()
#
#
# class Category(models.Model):
#     name_category = models.CharField(max_length=255, unique=True)
#
#
# class PostCategory(models.Model):
#     post = models.ForeignKey('Post', on_delete=models.CASCADE)
#     in_category = models.ForeignKey(Category, on_delete=models.CASCADE)
#
#
# class Post(models.Model):
#     news = "NS"
#     papers = "PP"
#     event_choose = [(news, "Новость"), (papers, "Статья")]
#     post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     categories = models.ManyToManyField(Category, through=PostCategory)
#     time_in_post = models.DateTimeField(auto_now_add=True)
#     event = models.CharField(choices=event_choose, max_length=2)
#     title = models.CharField(max_length=199)
#     post_text = models.TextField()
#     post_rating = models.IntegerField(default=0)
#
#     def like_post(self):
#         self.post_rating += 1
#         self.save()
#
#     def dislike_post(self):
#         self.post_rating -= 1
#         self.save()
#
#     def preview(self):
#         return self.post_text[:125:] + "..."
#
#
# class Comment(models.Model):
#     comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
#     time_in_comment = models.DateTimeField(auto_now_add=True)
#     comment_text = models.TextField(unique=True)
#     # А вдруг придут боты и начнут спам))))
#     comment_rating = models.IntegerField(default=0)
#
#     def like_comment(self):
#         self.comment_rating += 1
#         self.save()
#
#     def dislike_comment(self):
#         self.comment_rating -= 1
#         self.save()
