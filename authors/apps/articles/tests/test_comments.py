from rest_framework import status
from .basetests import BaseTest
import json


class TestComments(BaseTest):
    """
    Class to test comments
    """
    error = "Article does not exist"
    msg = "Comment or the Article was not found"
    body = "unsuccesful update either the comment orslug not found"
    msgg = 'unsuccesful update either the comment orslug not found'
    message = 'Comment deleted successfully'
    no_update = 'unsuccesful update either the comment orslug not found'

    def test_successful_comment_creation(self):
        """
        Test successful creation of a comment
        """
        response = self.create_comment()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_successful_comment_creation_by_id(self):
        """
        Test successful creation of a reply comment
        """
        response = self.create_child_comment()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsuccessful_comment_creation_by_id(self):
        """
        Test unsuccessful creation of a reply comment
        """
        response = self.create_child_comment_not_found()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'errors': {
                         'parent': ['Invalid pk "1" - object does not exist.']}})

    def test_unsuccessful_comment_creation(self):
        """
        Test unsuccessful creation of a comment
        """
        response = self.create_comment_fail()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], self.error)

    def test_successful_get_all_comments(self):
        """
        Test get all comments
        """
        response = self.get_all_comments()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsuccessful_delete_comment(self):
        """
        Test unsuccessful delete comment
        """
        response = self.delete_comment()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], self.msg)

    def test_successful_delete_comment(self):
        """
        Test successful delete comment
        """
        response = self.delete_comment_succefully()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'message': {
                         'body': [self.message]}})

    def test_update_comment_unsecceful(self):
        """
        Test update comment unsecceful
        """
        response = self.update_comment_unsuccefully()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {
                         'error': {'body': [self.no_update]}})

    def test_update_comment_successful(self):
        """
        Test update comment successful
        """
        response = self.update_comment_succefully()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_successful_get_one_comment(self):
        """
        Test one comment
        """
        response = self.get_all_comments()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_comment_not_found(self):
        """
        Test one comment not found
        """
        response = self.get_one_comment_not_found()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], self.msg)

    def test_successful_get_one_comment_by_id(self):
        """
        Test one comment
        """
        response = self.get_comments_by_id()
        self.assertEqual(response.status_code, status.HTTP_200_OK)