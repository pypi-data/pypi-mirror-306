from unittest import TestCase
from unittest.mock import patch
from certishop import WalliD  # Adjust the import based on your module structure

class TestWalliDLibrary(TestCase):
    def setUp(self):
        self.api_url = "https://demo.eidcmp.wallid.io/api/v1"
        self.api_token = "your_api_token"
        self.walliD = WalliD(self.api_url, self.api_token)

    @patch('requests.post')
    def test_create_ca(self, mock_post):
        # Set up mock response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "message": {
                "name": "CA Name",
                "admin_email": "admin@example.com",
                "creatorWA": "0x4289128eb6e3b298140845364fbec0f7344ffe8b",
                "contract_address": "0x99999999",
                "admin": [
                    "0x4289128eb6e3b298140845364fbec0f7344ffe8b"
                ],
                "issuerKey": {
                    "type": "jwk",
                    "jwk": {
                        "kty": "OKP",
                        "d": "Ho_2n9eidSDnKwKrw3pfxl_QYvBf-iLcIysR3ttsDlE",
                        "crv": "Ed25519",
                        "kid": "nDVD3o4MUzwPddZim_AQIkybSo3gc9pPsS06Ff3A0xU",
                        "x": "slQ0XLMtyvETG9GDZz_89ytjspNRsn7fNBcWvtWRsS8"
                    }
                },
                "issuerDid": "did:jwk:example_did",
                "_id": "670fb05a77d3b449d9e3b69f",
                "code": "0x172fde1d5fd586411af4939b776693e93235b1791d17a5d9d935c3886183b16d",
                "createdAt": "2024-10-16T12:23:54.517Z",
                "updatedAt": "2024-10-16T12:23:54.517Z",
                "cid": "670fb05a77d3b449d9e3b69f",
                "id": "670fb05a77d3b449d9e3b69f"
            }
        }

        wallet_address = "0x4289128eb6e3b298140845364fbec0f7344ffe8b"
        admin_email = "admin@example.com"
        response = self.walliD.create_ca(wallet_address, admin_email)

        # Print the CA ID, wallet address, and admin email
        cid = response.get('message', {}).get('id', 'N/A')  # Default to 'N/A' if not found
        print(
            f"Retrieving CA data:\n"
            f"CA ID: {cid}\n" 
            f"Wallet Address: {wallet_address}\n"
            f"Admin Email: {admin_email}\n"
        )

        mock_post.assert_called_once()
        self.assertEqual(response["message"]["admin_email"], admin_email)
        self.assertEqual(response["message"]["creatorWA"], wallet_address)

    @patch('requests.post')
    def test_create_template(self, mock_post):
        # Set up mock response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "cid": "66fd767cbd536ca460f33be4",
            "name": "template_name",
            "creatorWa": "0x4289128eb6e3b298140845364fbec0f7344ffe8b",
            "frontendProps": {
                "name": "Card",
                "repeatedAttributes": False,
                "currentLayout": "Card",
                "design": "Card",
            },
            "lang": "en",
            "template_chain": {
                "sig": []
            },
            "status": "active",
            "admin": [
                "0x4289128eb6e3b298140845364fbec0f7344ffe8b"
            ],
            "tid": "670fb92e77d3b449d9e3b6fe"
        }

        cid = "66fd767cbd536ca460f33be4"
        name = "template_name"
        wa = "0x4289128eb6e3b298140845364fbec0f7344ffe8b"
        frontend_props = {
            "components": [
                {"id": "component_id", "type": "text"}
            ],
            "currentLayout": "current_layout"
        }

        response = self.walliD.create_template(cid, name, wa, frontend_props)

        # Print the template ID, wallet address, and template name
        tid = response.get('tid', 'N/A')
        print(
            f"Retrieving Template Data:\n"
            f"CA ID: {cid}\n"
            f"Template ID: {tid}\n"
            f"Template Name: {name}\n"
            f"Wallet Address: {wa}\n"
            f"Frontend Props: {frontend_props}\n"
        )

        mock_post.assert_called_once()
        self.assertEqual(response["name"], name)
        self.assertEqual(response["creatorWa"], wa)

    @patch('requests.get')
    def test_fetch_template(self, mock_get):
        # Set up mock response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "cid": "66fd767cbd536ca460f33be4",
            "name": "Card",
            "creatorWa": "0x4289128eb6e3b298140845364fbec0f7344ffe8b",
            "frontendProps": {
                "name": "Card",
                "repeatedAttributes": False,
                "currentLayout": "Card",
                "design": "Card",
                "components": [
                    {"id": "component_id", "type": "text"}
                ],
                "layoutBackgroundColor": "#29969E",
                "backgroundFront": "http://127.0.0.1:3000/ftp/670fb92e77d3b449d9e3b6f8",
                "backgroundBack": "",
                "customTemplateName": "templateEditor",
                "preview": "http://127.0.0.1:3000/api/v1/assets/backgrounds/card-design.png",
                "conditions": []
            },
            "lang": "en",
            "template_chain": {
                "sig": []
            },
            "status": "active",
            "admin": [
                "0x4289128eb6e3b298140845364fbec0f7344ffe8b"
            ],
            "_id": "670fb92e77d3b449d9e3b6fe",
            "tid_sod": "0x32c854c8fd9dc2f46439c3aae7bf63fccbeec15185b7dadd4cdd4acd0dbde3f5",
            "createdAt": "2024-10-16T13:01:34.880Z",
            "updatedAt": "2024-10-16T13:01:34.880Z",
            "tid": "670fb92e77d3b449d9e3b6fe"
        }

        tid = "670fb92e77d3b449d9e3b6fe"
        response = self.walliD.fetch_template(tid)

        # Print the template details
        print(
            f"Fetching Template:\n"
            f"Template ID: {tid}\n"
            f"Template Details: {response}\n"
        )

        mock_get.assert_called_once()
        self.assertEqual(response["tid"], tid)

    @patch('requests.delete')
    def test_delete_template(self, mock_delete):
        # Set up mock response
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = {
            "tid": "670fb92e77d3b449d9e3b6fe"
        }

        tid = "670fb92e77d3b449d9e3b6fe"
        response = self.walliD.delete_template(tid)

        # Print the delete response
        print(
            f"Deleting Template:\n"
            f"Template ID: {tid}\n"
            f"Delete Response: {response} sueccesfully deleted!\n"
        )

        mock_delete.assert_called_once()
        self.assertEqual(response["tid"], tid)

    @patch('requests.post')
    def test_issue_credential(self, mock_post):
        # Set up mock response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "data": {
                "mgs": "The invite 670fb0d577d3b449d9e3b6a7 was sent!",
                "inviteId": "670fb0d577d3b449d9e3b6a7"
            },
            "credentialUrl": "openid-credential-offer://issuer.portal.walt.id/?credential_offer_uri=https%3A%2F%2Fissuer.portal.walt.id%2Fopenid4vc%2FcredentialOffer%3Fid%3Dc4d7f3f6-a8fb-4f89-8ca7-c2e9932dc3e4"
        }

        cid = "66fd767cbd536ca460f33be4"
        tid = "670fb92e77d3b449d9e3b6fe"
        waAdmin = "waAdmin_value"
        data = [{"key": "value"}]
        email = "user@domain.com"

        response = self.walliD.issue_credential(cid, tid, waAdmin, data, email)

        # Print the invite message and credential URL
        invite_message = response["data"]["mgs"]
        credential_url = response["credentialUrl"]
        print(
            f"Issuing Credential:\n"
            f"Invite ID: {invite_message}\n"
            f"Credential URL: {credential_url}\n"
            f"CID: {cid}\n"
            f"TID: {tid}\n"
        )

        mock_post.assert_called_once()
        self.assertEqual(response["data"]["mgs"], "The invite 670fb0d577d3b449d9e3b6a7 was sent!")
        self.assertIn("credential_offer_uri", credential_url)

    @patch('requests.post')
    def test_verify_credential(self, mock_post):
        # Set up mock response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "verificationUrl": "openid4vp://authorize?response_type=vp_token&client_id=https%3A%2F%2Fverifier.portal.walt.id%2Fopenid4vc%2Fverify&response_mode=direct_post&state=ClJIRQQu8FBr&presentation_definition_uri=https%3A%2F%2Fverifier.portal.walt.id%2Fopenid4vc%2Fpd%2FClJIRQQu8FBr&client_id_scheme=redirect_uri&client_metadata=%7B%22authorization_encrypted_response_alg%22%3A%22ECDH-ES%22%2C%22authorization_encrypted_response_enc%22%3A%22A256GCM%22%7D&nonce=f9ce4c7d-2804-4804-bc21-6e1fe199da60&response_uri=https%3A%2F%2Fverifier.portal.walt.id%2Fopenid4vc%2Fverify%2FClJIRQQu8FBr"
        }

        cid = "66fd767cbd536ca460f33be4"
        tid = "670fb92e77d3b449d9e3b6fe"
        credential_id = "credential_id"
        guid = "guid_value"

        response = self.walliD.verify_credential(credential_id, tid, guid)

        # Print the verification URL
        verification_url = response["verificationUrl"]
        print(
            f"Verifying Credential:\n"
            f"CA ID: {cid}\n"
            f"Template ID: {tid}\n"
            f"Certificate ID: {id}\n"
            f"Verification URL: {verification_url}\n"
        )

        mock_post.assert_called_once()
        self.assertIn("openid4vp://", verification_url)

if __name__ == "__main__":
    unittest.main()
