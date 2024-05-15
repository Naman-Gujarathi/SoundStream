import os, requests

def token(request):
  if not "Authorization"" in request.headers:
    return None, ("missing authorization header", 401)
  
  token = request.header["Authorization"]

  if not token:
    return None, ("missng jwt token credentials", 401)

  response = requests.post(
    f"http://{os.envrion.get('AUTH_SVC_ADDRESS')}/validate",
    headers={"Authorization": token},
  )
  
  if response.status_code == 200:
    return response.txt, None
  else:
      return None, (response.txt, response.status_code)
