#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/24 16:40
import json

from flask import g, jsonify, request
from flask import url_for, current_app
from flask_restful import Resource

from back import setting
from .errors import forbidden
from back.models import Article


def abort_if_not_exist(post_id):
    """
    操作之前需要保证操作的文章存在，否则返回 404
    :param post_id:
    :return:
    """
    desc = 'The post {} not exist.'.format(post_id)
    post = Article.query.get_or_404(post_id, description=desc)
    return post


class Post(Resource):
    """
    获取文章列表（分页展示）
    """

    def __init__(self):
        self.response_obj = {'status': 'success', 'code': 0}

    def get(self):
        page = request.args.get('page', 1, type=int)
        pagination = Article.query.order_by(Article.create_date.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
        )
        if pagination:
            # TODO：此处需要进一步查询
            posts = pagination.items

            prev_page = None
            if pagination.has_prev:
                prev_page = url_for('api.posts', page=page - 1, _external=True)
            next_page = None
            if pagination.has_next:
                next_page = url_for('api.posts', page=page + 1, _external=True)
            self.response_obj['posts'] = [post.to_json() for post in posts]
            self.response_obj['prev'] = prev_page
            self.response_obj['next'] = next_page
            self.response_obj['count'] = pagination.total
            # TODO: to_json 需要自写
            return jsonify(self.response_obj)
        else:
            self.response_obj['code'] = 1
            self.response_obj['status'] = 'failure'
            return self.response_obj, 500


class NewestPost(Resource):
    """
    最新文章
    """

    def __init__(self):
        self.response_obj = {'status': 'success', 'code': 0}

    def get(self):
        posts = Article.query.order_by(Article.create_date.desc()).limit(setting.LIMIT_NEW_POST_COUNT)
        if posts:
            self.response_obj['posts'] = [post.to_json() for post in posts]  # TODO:需要组装，不需要返回所有信息
            self.response_obj['count'] = setting.LIMIT_NEW_POST_COUNT
            return jsonify(self.response_obj)
        else:
            self.response_obj['code'] = 1
            self.response_obj['status'] = 'failure'
            return self.response_obj, 500


'''
1.5 避免多级 URL
常见的情况是，资源需要多级分类，因此很容易写出多级的 URL，比如获取某个作者的某一类文章。


GET /authors/12/categories/2
这种 URL 不利于扩展，语义也不明确，往往要想一会，才能明白含义。

更好的做法是，除了第一级，其他级别都用查询字符串表达。


GET /authors/12?categories=2
下面是另一个例子，查询已发布的文章。你可能会设计成下面的 URL。
GET /articles/published
查询字符串的写法明显更好。
GET /articles?published=true
'''


class HottestPost(Resource):  # TODO: 最新和最热好像没有必要写专门的接口 详见上面的注释
    """
    最热文章
    """

    def __init__(self):
        self.response_obj = {'status': 'success', 'code': 0}

    # TODO:此处需要根据不同条件编写
    '''
    如果记录数量很多，服务器不可能都将它们返回给用户。API应该提供参数，过滤返回结果。

    下面是一些常见的参数。
    
    ?limit=10：指定返回记录的数量
    ?offset=10：指定返回记录的开始位置。
    ?page=2&per_page=100：指定第几页，以及每页的记录数。
    ?sortby=name&order=asc：指定返回结果按照哪个属性排序，以及排序顺序。
    ?animal_type_id=1：指定筛选条件
    参数的设计允许存在冗余，即允许API路径和URL参数偶尔有重复。比如，GET /zoo/ID/animals 与 GET /animals?zoo_id=ID 的含义是相同的。
    '''

    def get(self):
        posts = Article.query.order_by(Article.view_counts.desc()).limit(setting.LIMIT_HOT_POST_COUNT)
        if posts:
            self.response_obj['posts'] = [post.to_json() for post in posts]  # TODO:需要组装，不需要返回所有信息
            self.response_obj['count'] = setting.LIMIT_NEW_POST_COUNT
            return jsonify(self.response_obj)
        else:
            self.response_obj['code'] = 1
            self.response_obj['status'] = 'failure'
            return self.response_obj, 500


class PostDetail(Resource):
    def __init__(self):
        self.response_obj = {'status': 'success', 'code': 0}

    def get(self, post_id):
        """
        获得指定ID对应的文章
        :param post_id: int,
        :return: json,
        """
        post = abort_if_not_exist(post_id)
        self.response_obj['data'] = post
        return jsonify(self.response_obj)

    def post(self, post_id):
        """
        创建指定id文章
        :return:
        """
        post = Article.query.get(post_id)
        if post:
            self.response_obj['error'] = 'Invalid post id.'
            self.response_obj['data'] = ''
            self.response_obj['msg'] = 'Create an exist post is impossible.'
            return jsonify(self.response_obj, 500)
        else:
            post = Article.from_json(request.json)
            post.author_id = g.current_user  # TODO:用户登录之后保存用户名称和用户id
            Article.insert_new_post(post)  # TODO:need func()
            # 服务器为新资源指派URL，并在响应的Location首部中返回
            return jsonify(post.to_json()), 201, {'Location': url_for('api.get_post', id=post.id, _external=True)}

    def put(self, post_id):
        """
        更新指定文章
        注意：必须是原作者，TODO:管理员可以折叠或隐藏？后期开发
        :param post_id:
        :return:
        """
        post = abort_if_not_exist(post_id)
        # if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
        if g.current_user != post.author_id:  # TODO:此处必须保证唯一
            return forbidden('Insufficient permissions')
        recvdata = json.loads(str(request.data, encoding="utf-8"))
        if recvdata:
            poster = recvdata['params']
            Article.update_post_by_id(post_id, poster)
        return jsonify(post.to_json())

    def delete(self, post_id):
        """
        删除指定文章
        :param post_id: int
        :return:
        """
        post = abort_if_not_exist(post_id)
        # if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
        if g.current_user != post.author_id:  # TODO:此处必须保证唯一，除了用户本人，管理员应该也可以删除
            return forbidden('Insufficient permissions')
        Article.delete_post(post)
        return jsonify(post.to_json())