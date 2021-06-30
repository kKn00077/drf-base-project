from rest_framework.test import APITestCase as TestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken


class APITestCase(TestCase):
    def _get_token(self, user):
        return AccessToken.for_user(user)

    def _get_authorization(self, user):
        return f"Bearer {self._get_token(user)}"

    def _set_argument(self, url, data, user, content_format):
        kwargs = {"path": url, "format": content_format}

        if data is not None:
            kwargs.update({"data": data})

        if user is not None:
            kwargs.update({"HTTP_AUTHORIZATION": self._get_authorization(user=user)})

        return kwargs

    def get(
        self,
        url,
        data=None,
        expect_status=status.HTTP_200_OK,
        user=None,
        has_pagination=False,
        content_format="json",
    ):
        res = self.client.get(
            **self._set_argument(
                url=url,
                data=data,
                user=user,
                content_format=content_format,
            )
        )
        self.assertEqual(res.status_code, expect_status, msg=res.json())
        result = res.json()

        if has_pagination:
            if result.get("results") is not None:
                self.assertIsInstance(result["results"], list)
            else:
                self.assertIsInstance(result, list)

        return result

    def post(
        self,
        url,
        data={},
        expect_status=status.HTTP_200_OK,
        user=None,
        content_format="json",
    ):
        res = self.client.post(
            **self._set_argument(
                url=url,
                data=data,
                user=user,
                content_format=content_format,
            )
        )

        self.assertEqual(res.status_code, expect_status, msg=res.json())
        result = res.json()

        return result

    def delete(
        self,
        url,
        data=None,
        expect_status=status.HTTP_204_NO_CONTENT,
        user=None,
        content_format="json",
    ):
        res = self.client.delete(
            **self._set_argument(
                url=url,
                data=data,
                user=user,
                content_format=content_format,
            )
        )
        self.assertEqual(res.status_code, expect_status)

    def check_field_exists(self, data, fields=[]):
        for field in fields:
            self.assertIn(field, data)
