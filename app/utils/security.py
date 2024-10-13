from api import api_request

def login_user(username, password):
    try:
        response = api_request("POST", "/login", data={"username": username, "password": password})
        if response and response.get("status") == "success":
            return {"status": "success", "user": response.get("user")}
        else:
            return {"status": "error", "detail": response.get("detail", "Invalid credentials")}
    except Exception as e:
        return {"status": "error", "detail": str(e)}