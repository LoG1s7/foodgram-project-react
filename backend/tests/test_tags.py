import pytest
from recipes.models import Tag


class TestTagsApi:

    @pytest.mark.django_db(transaction=True)
    def test_tags_not_found(self, client, tag_1):
        response = client.get('/api/tags/')

        assert response.status_code != 404, (
            'Страница `/api/tags/` не найдена, '
            'проверьте этот адрес в *urls.py*'
        )
