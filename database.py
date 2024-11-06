from supabase import create_client, Client

url: str = "https://qmhmguogemmmoqnynhje.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFtaG1ndW9nZW1tbW9xbnluaGplIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA4ODA1MzYsImV4cCI6MjA0NjQ1NjUzNn0.BAr__7pEyuQjdMgJkzNFWj4_1ANTpIb4Tu1cZiTpJ7o"
supabase: Client = create_client(url, key)