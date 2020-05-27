from unittest.mock import patch

from django.http import HttpRequest, JsonResponse
from django.test import TestCase

from api.v2.views import misc

# TODO: figure out why the request.POST dictionary gets reset, thus making the test fail
# class Misc_Feedback_TestCase(TestCase):
#     def setUp(self):
#         self.request = HttpRequest()
#         self.request.method = "POST"
#         self.request.POST = QueryDict(mutable=True)
#         self.request.POST.__setitem__("from_name", "Mr. Login")
#         self.request.POST.__setitem__("from_email", "sign.in@login.me")
#         self.request.POST.__setitem__("reason", "Letter of Resignation")
#         self.request.POST.__setitem__("comments", "My time has finally come. Goodbye.")

#     @patch("api.v2.views.misc.email_feedback", autospec=True)
#     def test_send_feedback_forwarded(self, mock_email_feedback):
#         self.request.META = {"HTTP_X_FORWARDED_FOR": "vonx.io,somethingelse"}

#         print("11111111111111", self.request.POST)

#         result = misc.send_feedback(self.request)

#         mock_email_feedback.assert_called_once_with(
#             "vonx.io",
#             "Mr. Login",
#             "sign.in@login.me",
#             "Letter of Resignation",
#             "My time has finally come. Goodbye.",
#         )

#         self.assertEqual(
#             result, JsonResponse({"status": "ok"}), "The JsonResponse should match."
#         )

# @patch("api.v2.views.misc.email_feedback", autospec=True)
# def test_send_feedback_remoteaddr(self, mock_email_feedback):
#     self.request.META["REMOTE_ADDR"] = "REMOTE_ADDR"

#     result = misc.send_feedback(request=self.request)

#     mock_email_feedback.assert_called_once_with(
#         "vonx.io",
#         "Mr. Login",
#         "sign.in@login.me",
#         "Letter of Resignation",
#         "My time has finally come. Goodbye.",
#     )

#     self.assertEqual(
#         result, JsonResponse({"status": "ok"}), "The JsonResponse should match."
#     )


class Misc_Quickload_TestCase(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.method = "GET"

    @patch("api.v2.views.misc.model_counts", autospec=True)
    @patch("api.v2.views.misc.record_count", autospec=True)
    @patch("api.v2.views.misc.solr_counts", autospec=True)
    def test_quickload(self, mock_solr_counts, mock_record_counts, mock_model_counts):
        mock_solr_counts.return_value = {
            "total_indexed_items": 18,
            "active": 3,
            "registrations": 4,
            "last_month": 1,
            "last_week": 1,
            "last_24h": 1,
        }
        mock_record_counts.return_value = 6
        mock_model_counts.return_value = 6
        result = misc.quickload(self.request)
        json_result = result.content

        self.assertEqual(
            json_result,
            JsonResponse(
                {
                    "counts": {
                        "claim": 6,
                        "credential": 6,
                        "credentialtype": 6,
                        "issuer": 6,
                        "topic": 6,
                        "name": 6,
                        "actual_credential_count": 6,
                        "actual_name_count": 6,
                        "actual_topic_count": 6,
                        "actual_item_count": 18,
                    },
                    "credential_counts": {
                        "total_indexed_items": 18,
                        "active": 3,
                        "registrations": 4,
                        "last_month": 1,
                        "last_week": 1,
                        "last_24h": 1,
                    },
                    "demo": False,
                    "indexes_synced": True,
                }
            ).content,
            "The JsonResponse should match.",
        )
