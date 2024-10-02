from supabase import create_client, Client

url: str = "https://cwiespeponefxujkahlm.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3aWVzcGVwb25lZnh1amthaGxtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg2OTg3ODUsImV4cCI6MjAzNDI3NDc4NX0.rGSmo-gYeCnNFoYfN_0fJsE_z7knoAxYU9BoiDduP5c"
supabase: Client = create_client(url, key)