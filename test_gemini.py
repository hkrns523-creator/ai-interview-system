import google.generativeai as genai

genai.configure(
    api_key="AIzaSyDNhMiLrmp-LuGKo_fixpa6EcqntNoax4Q"
)

models = genai.list_models()

for model in models:
    print(model.name)