import unittest
from parser import parse_roles_and_users
from db import init_db
from subordinate_search import subordinate_search


class TestUserHierarchy(unittest.TestCase):
    def assert_subordinate(self, db: dict, user_id: int, subordinate_user_ids: list):
        subordinate_users = subordinate_search(db, user_id)
        user_ids_under = sorted(set([u.id for u in subordinate_users]))
        assertion = user_ids_under == sorted(subordinate_user_ids)
        if assertion != True:
            import pdb; pdb.set_trace()

        self.assertTrue(assertion)

    def setUp(self):
        roles_filepath = "resources/roles.json"
        users_filepath = "resources/users.json"
        roles, users = parse_roles_and_users(roles_filepath, users_filepath)
        self.root_user_id = 1
        self.db = init_db(roles, users)

    def test_who_is_root(self):
        """
        Assert that the RoleID 1 is the root role
        """

        self.assertTrue(self.db['roles'][self.root_user_id].is_root_role)

        # Assert that only Adam Admin has the root role
        for uid, user in self.db['users'].items():
            if uid == self.root_user_id:
                self.assertTrue(user.role_id == self.root_user_id)
                self.assertTrue(user.name == "Adam Admin")
            else:
                self.assertTrue(user.role_id != self.root_user_id)

        print("Test that only Adam Admin has the only role role: OK")

    def test_root_must_be_above_all(self):
        """
        Root has subordinates except himself
        """
        self.assert_subordinate(self.db, self.root_user_id, [2,3,4,5])
        print("Test that Root is above all others: OK")

    def test_employee_and_trainer_has_no_one(self):
        """
        Employee and trainer do not have anyone under them
        """

        # Emily Employee do not have anyone under
        self.assert_subordinate(self.db, 2, [])
        # Steve Trainer do not have anyone under
        self.assert_subordinate(self.db, 5, [])
        print("Test that employee and trainee do not have anyone under them: OK")


    def test_supervisor(self):
        """
        Supervisor is above Emily and Steve
        """
        self.assert_subordinate(self.db, 3, [4, 5])
        print("Test supervisor is above Emily and Steve: OK")

if __name__ == '__main__':
    unittest.main()
