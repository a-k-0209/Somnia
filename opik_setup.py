# import os
# import opik


# def configure_opik():
#     # Set project name for Opik
#     os.environ["OPIK_PROJECT_NAME"] = "Somnia"
    
#     api_key = os.environ.get("OPIK_API_KEY")
#     if api_key and api_key != "test_key":
#         try:
#             opik.configure(api_key=api_key)
#         except Exception as e:
#             print(f"Opik configuration failed: {e}")
#             print("Continuing without Opik tracing...")
#     else:
#         print("No valid Opik API key found. Continuing without tracing...")


