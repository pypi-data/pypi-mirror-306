from flask import Flask
from flask_supabase import Supabase

app = Flask(__name__)
app.config["SUPABASE_URL"] = "https://vzdbuiarkymigvwdqapm.supabase.co"
app.config["SUPABASE_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ6ZGJ1aWFya3ltaWd2d2RxYXBtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjE0OTkzNDgsImV4cCI6MjAzNzA3NTM0OH0.AApaA0aMDWUwYbRy70sHm-En0ZR_fg0Z5TExiAsdsQ4"
app.config["SUPABASE_CLIENT_OPTIONS"] = {
    "postgrest_client_timeout": 10
}  # Example options

supabase = Supabase(app)



@app.route("/test_supabase")
def test_supabase():
    import pdb
    pdb.set_trace()
    try:
        # Access the Supabase client directly
        client = supabase.client
        
        
        # Perform a simple operation, like listing tables or fetching a user
        # This assumes you have a method to list tables or similar
        response = client.table('reservations').select('*').execute()
        
        return f"Supabase is working: {response.data}"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
