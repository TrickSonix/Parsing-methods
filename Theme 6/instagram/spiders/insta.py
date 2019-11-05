# -*- coding: utf-8 -*-
import re
import json
import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import urlencode, urljoin
from copy import deepcopy

class InstaSpider(scrapy.Spider):
    name = 'insta'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    variables_base = {'fetch_mutual': 'false', "include_reel": 'true', "first": 100}
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    following = {}

    def __init__(self, login, pwd, users, *args, **kwargs):
        self.login = login
        self.pwd = pwd
        self.users = users
        self.query_hash = 'd04b0a864b4b54837c0d870b0e77e076'
        super().__init__(*args, **kwargs)

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
        yield scrapy.FormRequest(
            inst_login_link,
            method='POST',
            callback=self.parse_users,
            formdata={'username': self.login, 'password': self.pwd},
            headers={'X-CSRFToken': csrf_token}
            )

    def parse_users(self, response: HtmlResponse):
        json_body = json.loads(response.body)
        if json_body.get('authenticated'):
            for user in self.users:
                yield response.follow(urljoin(self.start_urls[0], user),
                                      callback=self.parse_user, 
                                      cb_kwargs={'user': user})

    def parse_user(self, response: HtmlResponse, user):
        user_id = self.fetch_user_id(response.text, user)
        user_vars = deepcopy(self.variables_base)
        user_vars.update({'id': user_id})
        yield response.follow(self.make_graphql_url(user_vars, self.query_hash),
                              callback=self.parse_following, 
                              cb_kwargs={'user_vars': user_vars, 'user': user}
                              )

    def parse_following(self, response, user_vars, user):
        data = json.loads(response.body)
        if self.following.get(user):
            self.following[user]['edges'].extend(data['data']['user']['edge_follow']['edges'])
        else:
            self.following[user] = {'edges': data['data']['user']['edge_follow']['edges']}
        if data['data']['user']['edge_follow']['page_info']['has_next_page']:
            user_vars.update({'after': data['data']['user']['edge_follow']['page_info']['end_cursor']})
            next_page = self.make_graphql_url(user_vars, self.query_hash)
            yield response.follow(next_page,
                                callback=self.parse_following, 
                                cb_kwargs={'user_vars': user_vars, 'user': user}
                                )
        else:
            for username in self.following[user]['edges']:
                yield response.follow(urljoin(self.start_urls[0], username['node']['username']),
                                              callback=self.parse_user_posts,
                                              cb_kwargs={'user': username['node']['username']}
                                              )
            if len(self.following) == len(self.users):
                yield self.following

    def parse_user_posts(self, response: HtmlResponse, user):
        user_id = self.fetch_user_id(response.text, user)
        user_vars = {'first': 100}
        user_vars.update({'id': user_id})
        posts_query_hash = '2c5d4d8b70cad329c4a6ebe3abb6eedd'
        yield response.follow(self.make_graphql_url(user_vars, posts_query_hash),
                              callback=self.parse_posts, 
                              cb_kwargs={'user_vars': user_vars, 'user': user}
                              )

    def parse_posts(self, response: HtmlResponse, user_vars, user):
        data = json.loads(response.body)
        result = {f'{user}_posts': data['data']['user']['edge_owner_to_timeline_media']['edges']}
        yield result

    def fetch_user_id(self, text, username):
        """Используя регулярные выражения парсит переданную строку на наличие
        `id` нужного пользователя и возвращет его."""
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

    def fetch_csrf_token(self, text):
        """Используя регулярные выражения парсит переданную строку на наличие
        `csrf_token` и возвращет его."""
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def make_graphql_url(self, user_vars, query_hash):
        """Возвращает `url` для `graphql` запроса"""
        result = '{url}query_hash={query_hash}&{variables}'.format(
            url=self.graphql_url, query_hash=query_hash,
            variables=urlencode(user_vars)
        )
        return result
