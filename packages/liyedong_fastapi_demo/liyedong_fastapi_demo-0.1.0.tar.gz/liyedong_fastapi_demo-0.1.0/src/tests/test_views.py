import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response

from liyedong_fastapi_demo.models import Article
from liyedong_fastapi_demo.schemas import ModelType


def test_docs(client):
    """Test view"""
    response = client.get('/docs')
    assert response.status_code == 200


class BaseTest:
    version = 'v1'
    base_url: str
    model: ModelType

    @pytest.fixture()
    def init_data(self):
        pass

    def url(self, pk: int = None) -> str:
        url_split = ['api', self.version, self.base_url]
        if pk:
            url_split.append(str(pk))
        return '/'.join(url_split)

    def assert_response_ok(self, response: Response):
        assert response.status_code == 200

    def test_get(self, client, session, init_data):
        count = session.query(self.model).count()
        response = client.get(self.url())
        self.assert_response_ok(response)
        assert count == len(response.json())

    def test_get_by_id(self, client, session, init_data):
        obj = session.query(self.model).first()
        response = client.get(self.url(obj.id))
        self.assert_response_ok(response)
        assert jsonable_encoder(obj) == response.json()

    def test_delete(self, client, session, init_data):
        # 初始计数
        initial_count = session.query(self.model).count()

        # 获取待删除对象
        obj = session.query(self.model).first()
        assert obj is not None, "没有找到需要删除的对象"

        # 发送删除请求
        response = client.delete(self.url(obj.id))
        self.assert_response_ok(response)

        # 提交事务确保变更持久化
        session.commit()

        # 清除会话缓存，重新获取最新对象
        session.expire_all()

        # 删除后的计数
        after_count = session.query(self.model).count()
        assert after_count == initial_count - 1, f"Expected count {initial_count - 1}, but got {after_count}"


class TestArticle(BaseTest):
    model = Article
    base_url = 'articles'

    @pytest.fixture()
    def init_data(self, init_article):
        pass

    def test_create(self, client, session, init_data):
        response = client.post(
            self.url(),
            json={'title': 'xxx'}
        )
        self.assert_response_ok(response)
        assert response.json().get('title') == 'xxx'

    def test_patch(self, client, session, init_data):
        obj = session.query(Article).first()
        response = client.patch(self.url(obj.id), json={'body': 'xxx'})
        self.assert_response_ok(response)
        assert response.json().get('body') != obj.body