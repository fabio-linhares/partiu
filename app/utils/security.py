from api import api_request

def login_user(username, password):
    try:
        response = api_request("POST", "/login", data={"username": username, "password": password})
        if response and "access_token" in response:
            return {"status": "success", "user": response}
        else:
            return {"status": "error", "detail": "Invalid credentials"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}