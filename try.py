import requests

# -----------------------------------------------------------
# 1. Your tokens from HackerRank
# -----------------------------------------------------------
ACCESS_TOKEN      = "cb14cf0a7654375c50b8a6053cb84ad958f8f488e08a1b9291568ee0bb43d9cc"
JWT_ACCESS_TOKEN  = "eyJraWQiOiJkLTE3NTgxOTcxNjU3NjgiLCJ0eXAiOiJKV1QiLCJ2ZXJzaW9uIjoiNCIsImFsZyI6IlJTMjU2In0.eyJpYXQiOjE3NjQ3NDg3NTcsImV4cCI6MTc2NDc0OTM1Nywic3ViIjoiNzM0OGJlYjAtNWRjMi00MDRhLWI0NzQtOTYxNjg0NzBmZmU4IiwidElkIjoicHVibGljIiwic2Vzc2lvbkhhbmRsZSI6ImY3ZTJhMmMzLTdlZTctNDhkNC05OTE3LWEwMjljNjAwODhmZCIsInJlZnJlc2hUb2tlbkhhc2gxIjoiMTViOTNiZmExYTcwZmU3YjM0MjM2MDVjMjRkZjgwN2MwNmNiOTRjYzI2MmI0OWU3ZDllYTA1YTJhNDlhYzM1MiIsInBhcmVudFJlZnJlc2hUb2tlbkhhc2gxIjoiNzJkNmI5NGIyNWFkZjc4MzgwZjRmZDQxYzA1MGE1NDhmMzNlMmUyM2Q1MDkxZmE3MGI1N2NmOWE1NDI3OWU4NyIsImFudGlDc3JmVG9rZW4iOm51bGwsImNvbXBhbnlfaWQiOiI4Mzc0NzJkNC01ZDcwLTRkZjUtOTEwYi1mZWY2MTk1ODAzNDgiLCJpc3MiOiJodHRwczovL2F1dGguaGFja2VycmFuay5jb20vYXV0aC9zdCIsImxlZ2FjeV9jb21wYW55X2lkIjo0NjIyOTAsImxlZ2FjeV9pZCI6MTQyNTUzNiwic2NvcGUiOlsiY2FuZGlkYXRlOmNlczpldmVudDpjcmVhdGUiLCJwbGF0Zm9ybTphbm9ueW1vdXM6cmVhZCIsImFpLXBsYXRmb3JtOmZyZWUiLCJoYWNrZXJyYW5rLWZvci13b3JrIiwiaW5zaWdodHMtc2VydmljZSIsImZsZXgtcm9sZXMiLCJzb2UiXSwic3QtZXYiOnsidCI6MTc2NDczMzk2ODQzNCwidiI6ZmFsc2V9fQ.YC6WEhLrdgsyjUg_wdAPB6wWiCQYCWr4tqdfxko__nBTdKxuNkBKiVHhGljy0A-GbOsEJCOgwcR3WC6IyV-XNX0rBMXb-ksXf85Amlme-JMLVtNMfS0AUWn6i20PzCFBfZEuM50HfsPMbahxdxvFhW9xcOKkvKodtpMCDTCuII-TPCotlIjeytARMSDse5d46eABOO5vth5Scu10cPTCZsy8K0pTsLdqHevtcDI0vGsUsJYxFV_pFx27I1yoaXY2-n1j6MN5XzePXDezl33j2DQr-1CO6Ayuf3B0A98eoB0JpQAnz9XP4711JoJgFtk01OeKWIF51Zmptt10xqdvQg"
JWT_REFRESH_TOKEN = "WUhQb1dCWEw5RlVYTE1Oa3lBQmdlM0pSeDBkUi9hZ1p1akp0N2dMNHlTMlVMbm9OU0cwbFNOOXkzRFpzVXhEaFZJM1hOd2ZpeWpYS0U3bXFSaERYNy9hbThVK3hIQkZrdDQ4YjdjSU4wdktaOHd6am5NaGI4SDBaRzQ4cG12eE82SnVCMUhtRnlNVXRMVWpnUzN1NkJRZzJxa1hGU0I4dG9SR3BhRitFY2JxamMyV21GUmNYbnR3UDNCb0FjdmdoU1VWZ3k0VW02WGF3ZE1wblhvTnJ3bVkxbFUyaktGWTF3ekFOYUplNTNicWFoMXlNb1VPQmpkZ2doZzlmODkyTUFxMWN4cGxsQldnekFqVUZNYUFqR0hYUlJBWE1nS0c0ZEJ6YmZQdlMrQU9qNmtXT0dxMEFiRGNWYnhKZlY5bHdjNVV6bWx2NU9DQzR5MndnRjZiRHM2TlozS3FwdTNSV0ZXMWJnbHM3ZjE2L0hvZm5YY1A2LytxZXh4Y3FQVjRscDhRL2I5MFQvaEVrWURBZi4yODlkMTdhMGU0OGNmN2IyNzg3YTUwZDNkZDliZDA0NjhjZTkwYWVhNzdiMjUxM2RkMmZhMjYwYTlmNTJlN2M1LlYy"
API_TOKEN         = "8262c4229d2834d93bf2f459e4df060bfc4c116a102a8163bb602aa5dc9ca64f"

# -----------------------------------------------------------
# 2. Common headers required for authenticated requests
# -----------------------------------------------------------
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "X-Auth-Token": API_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json",
    # HackerRank Enterprise APIs also accept these:
    "x-jwt-token": JWT_ACCESS_TOKEN,
    "x-refresh-token": JWT_REFRESH_TOKEN
}

# -----------------------------------------------------------
# 3. Example endpoint: Get All Tests (HackerRank for Work)
# -----------------------------------------------------------
url = "https://www.hackerrank.com/x/api/v3/tests"

response = requests.get(url, headers=headers)

print("Status:", response.status_code)
print("Response:")
print(response.json())
