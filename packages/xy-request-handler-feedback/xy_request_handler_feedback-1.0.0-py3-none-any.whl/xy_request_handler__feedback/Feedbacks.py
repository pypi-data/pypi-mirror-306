# -*- coding: UTF-8 -*-
__author__ = "余洋"
"""
	该类作为
"""
import os
import json
import tempfile
from xy_django_app_feedback.models import *
from xy_django_app_resource.models import *
from django.core.files import File  # you need this somewhere

from xy_request_handler_api.Api import Api


class Feedback(Api):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def get(self):
        self.operation()

    def post(self):
        self.operation()

    @property
    def username(self):
        return self.get_argument("username", "")

    @property
    def mobile(self):
        return self.get_argument("mobile", "")

    @property
    def email(self):
        return self.get_argument("email", "")

    @property
    def text(self):
        return self.get_argument("text", "")

    @property
    def qq(self):
        return self.get_argument("qq", "")

    @property
    def wechat(self):
        return self.get_argument("wechat", "")

    @property
    def weibo(self):
        return self.get_argument("weibo", "")

    @property
    def dingding(self):
        return self.get_argument("dingding", "")

    @property
    def facebook(self):
        return self.get_argument("facebook", "")

    @property
    def google(self):
        return self.get_argument("google", "")

    @property
    def twitter(self):
        return self.get_argument("twitter", "")

    def operation(self):
        responseDict = {"data": {}, "message": "发送成功", "code": 0}
        # try:
        image_files = []
        try:
            # file_metas = self.request.files.get(
            #     "file"
            # )  # 提取表单中‘name’为‘file’的文件元数据
            if self.request.files != None:
                for file_key in self.request.files:
                    file_meta = self.request.files.get(file_key)[0]
                    filename = file_meta.get("filename")
                    body = file_meta.get("body")
                    suffix = os.path.splitext(filename)[-1]
                    temp_file = tempfile.mkdtemp()
                    temp = tempfile.NamedTemporaryFile(
                        suffix=suffix, prefix=None, dir=temp_file, delete=True
                    )
                    temp.write(body)
                    image_files.append(temp)
        except:
            image_files = []
        if self.text != None and len(str(self.text)) != "":
            feedback = MFeedback.objects.create()
            feedback.username = self.username
            feedback.email = self.email
            feedback.mobile = self.mobile
            feedback.wechat = self.wechat
            feedback.qq = self.qq
            feedback.facebook = self.facebook
            feedback.twitter = self.twitter
            feedback.google = self.google
            feedback.weibo = self.weibo
            feedback.text = self.text
            if len(image_files) > 0:
                for image_file in image_files:
                    image = MImage.objects.create()
                    image_file_File = File(
                        image_file, os.path.split(image_file.name)[-1]
                    )
                    image.image = image_file_File
                    image.save()
                    image_file.close()
                    feedback.images.add(image)
            feedback.save()
        # except:
        #     responseDict["code"] = "1"
        #     responseDict["message"] = "发送失败"

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        return self.write(json.dumps(responseDict))
