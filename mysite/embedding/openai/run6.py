import openai

def generate_prompt(original_text):
    prompt = """Generate the tl;dr for the input text.
    input: A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei.
    output: Neutron stars are the collapsed cores of massive supergiant stars, with a radius of around 10 kilometres and a mass of 1.4 solar masses. They are formed from the supernova explosion of a massive star combined with gravitational collapse, compressing the core beyond white dwarf star density.
    input: {}
    output:"""
    return prompt.format(original_text)


def run_it_6(original_text):
    print(original_text)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(original_text),
        temperature=0,
        max_tokens=1000
    )
    print(response)
    return response
