from pages.auth import Auth

# Get Cfid and Cftoken
auth = Auth()
auth.get_tokens()
auth.login()
auth.get_home()