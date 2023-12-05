"""
backend/tests/test_user_service.py

Contains the unit tests for the user service
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from backend.services import UserService


class UserServiceTests(TestCase):
    """
    UserServiceTests holds unit tests for UserService
    """

    def setUp(self):
        self.service = UserService()

    @staticmethod
    def createUser(name, email):
        """
        Helper which creates a user with the following parameters
        :param str name: The username of the user
        :param str email: The email of the user
        :return: the user
        :rtype: User"""
        user = User(username=name, email=email)
        user.save()
        return user

    def test_get_user_by_id_user_existing(self):
        """Verifies whether get_user_by_id returns the expected user if it exists"""
        user = self.createUser("test-name", "test@mail.de")
        user_to_test = self.service.get_user_by_id(user.id)
        self.assertEqual(user_to_test, user)

    def test_get_user_by_id_user_not_existing(self):
        """Verifies whether get_user_by_id raises a ObjectDoesNotExist if user does not exist"""
        with self.assertRaises(ObjectDoesNotExist):
            id_with_no_user = 99999999999
            self.service.get_user_by_id(id_with_no_user)

    def test_update_user_no_updates(self):
        """Verifies whether update_user does not update the email or password if no parameters where given the method"""
        user = self.createUser("test-name", "test@mail.de")
        self.service.update_user(user)
        user_to_test = self.service.get_user_by_id(user.id)
        self.assertEqual(user_to_test.username, "test-name")
        self.assertEqual(user_to_test.email, "test@mail.de")
        self.assertEqual(user_to_test.password, "")

    def test_update_user_with_updates(self):
        """Verifies whether update_user does update the email or password if parameters where given the method"""
        user = self.createUser("test-name", "test@mail.de")
        self.service.update_user(user, email="new-test@mail.de", password="new-password")
        user_to_test = self.service.get_user_by_id(user.id)
        self.assertEqual(user_to_test.username, "test-name")
        self.assertEqual(user_to_test.email, "new-test@mail.de")
        self.assertTrue(user_to_test.check_password("new-password"))

    def test_update_user_falsy_mail(self):
        """Verifies whether update_user raises a validation error if a falsy mail adresse is given"""
        user = self.createUser("test-name", "test@mail.de")
        with self.assertRaisesMessage(ValidationError, "['Enter a valid email address.']"):
            self.service.update_user(user, email="new-test@falsy-domain")

    def test_update_user_falsy_password(self):
        """Verifies whether update_user raises a validation error if a falsy mail password is given"""
        user = self.createUser("test-name", "test@mail.de")
        with self.assertRaisesMessage(ValidationError,
                                      "['This password is too short. It must contain at least 8 characters.', "
                                      "'This password is too common.']"):
            self.service.update_user(user, password="a")
