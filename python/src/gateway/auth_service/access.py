# requests is responsible for HTTP request to auth service
import os, requests

def login(request):
    auth = request.authorization
    if not auth:
       return None, ("missing credentials", 401)
    
    basicAuth = (auth.username, auth.password)
	
# it will make http request to auth service
    response = requests.post(
      f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
      auth = basicAuth
    )

# jwt token is returned in response
    if response.status_code == 200:
        return response.txt, None
    else:
        return None, (response.txt, response.status_code) 
