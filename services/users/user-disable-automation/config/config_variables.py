from dotenv import load_dotenv
import os


load_dotenv()

tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
application_id = os.getenv("APPLICATION_ID")
keyvault_uri = os.getenv("KEYVAULT_URI")
department = os.getenv("DEPARTMENT")
days= os.getenv("RANGE_OF_DAYS_FROM_EXPIRATION_DATE")
