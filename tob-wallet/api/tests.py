from rest_framework.test import APITestCase

from .models import WalletItem


class OpportunityAPITests(APITestCase):

    # With fixture
    fixtures = ['test_data.json']

    test_userid = "wall-e"
    test_password = "pass1234"

    def get_auth_token(self, userid, password):
        response = self.client.post('/api/v1/api-token-auth/', data={"username":userid, "password":password})
        json_data = response.json()
        token = 'Token {}'.format(json_data["token"])
        return token

    def test_list_claims(self):
        # initial test should fail  unauthorized
        response = self.client.get('/api/v1/keyval/Rust_Wallet/rust_claim/')
        self.assertEqual(response.status_code, 401)

        # get a token to authenticate requests
        token = self.get_auth_token(self.test_userid, self.test_password)

        # authenticated request should pass
        response = self.client.get('/api/v1/keyval/Rust_Wallet/rust_claim/',
                                   HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        claim = response.data[0]
        self.assertEqual(claim['id'], 1)
        self.assertEqual(claim['item_id'], '968522')

        self.assertContains(response, 'wallet_name')

    def test_get_claim(self):
        # get a token to authenticate requests
        token = self.get_auth_token(self.test_userid, self.test_password)

        # authenticated request should pass
        response = self.client.get('/api/v1/keyval/Rust_Wallet/rust_claim/506034/',
                                   HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        claim = response.data[0]
        self.assertEqual(claim['id'], 2)
        self.assertEqual(claim['item_id'], '506034')

    def test_create_claim(self):
        # get a token to authenticate requests
        token = self.get_auth_token(self.test_userid, self.test_password)

        # new claim data
        new_claim = {}
        new_claim['wallet_name']  = 'New_Test_Wallet'
        new_claim['item_type']    = 'Test_A_Claim'
        new_claim['item_id']      = '9876543210abcdef'
        new_claim['item_value']   = '{"this":"is", "a":"claim", "from":"python"}'
        new_claim['created_date'] = '2018-03-13T23:53:37.114Z'

        # authenticated request should pass
        response = self.client.post('/api/v1/keyval/',
                                   HTTP_AUTHORIZATION=token,
                                    data=new_claim)
        self.assertEqual(response.status_code, 201)

        # new get it!
        response = self.client.get('/api/v1/keyval/New_Test_Wallet/Test_A_Claim/9876543210abcdef/',
                                   HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        claim = response.data[0]
        self.assertEqual(claim['item_id'], '9876543210abcdef')

    def test_update_claim(self):
        # get a token to authenticate requests
        token = self.get_auth_token(self.test_userid, self.test_password)

        # new claim data
        new_claim = {}
        new_claim['wallet_name']  = 'New_Test_Wallet'
        new_claim['item_type']    = 'Test_U_Claim'
        new_claim['item_id']      = 'a_claim_to_update'
        new_claim['item_value']   = '{"this":"is", "a":"claim", "from":"python"}'
        new_claim['created_date'] = '2018-03-13T23:53:37.114Z'

        # authenticated request should pass
        response = self.client.post('/api/v1/keyval/',
                                   HTTP_AUTHORIZATION=token,
                                    data=new_claim)
        self.assertEqual(response.status_code, 201)

        # new get it!
        response = self.client.get('/api/v1/keyval/New_Test_Wallet/Test_U_Claim/a_claim_to_update/',
                                   HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        claim = response.data[0]
        self.assertEqual(claim['item_id'], 'a_claim_to_update')

        # now update it!
        new_claim['item_value']   = '{"this":"is", "another":"claim", "updated_from":"python"}'
        response = self.client.put('/api/v1/keyval/{}/'.format(claim['id']),
                                   HTTP_AUTHORIZATION=token,
                                    data=new_claim)
        self.assertEqual(response.status_code, 200)

        # new get it again!
        response = self.client.get('/api/v1/keyval/New_Test_Wallet/Test_U_Claim/a_claim_to_update/',
                                   HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        claim = response.data[0]
        self.assertEqual(claim['item_id'], 'a_claim_to_update')
        self.assertEqual(claim['item_value'], '{"this":"is", "another":"claim", "updated_from":"python"}')


