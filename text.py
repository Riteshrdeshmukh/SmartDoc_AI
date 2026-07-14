import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6K4V5a3i5rfGTOrRB3ekEhWnbT_HLC1RjFdbJ6x8DetKg")

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("Hello")

print(response.text)

