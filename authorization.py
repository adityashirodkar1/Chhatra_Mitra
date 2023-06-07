import tekore as tk
def authorize():
 CLIENT_ID = '7cdff450afd9415c8e078323b464e539'
 CLIENT_SECRET = '102c0917f7c944ea89f66d3f7d85e467'
 app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
 return tk.Spotify(app_token)