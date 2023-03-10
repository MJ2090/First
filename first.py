import openai

def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(animal.capitalize())

response = openai.Completion.create(
  model="text-davinci-003",
  prompt=generate_prompt("Lion"),
  temperature=0.6
)

print(999)
print(response)
