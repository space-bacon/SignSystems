from openai import OpenAI
import os
import re
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image

# Set your OpenAI API key
openai.api_key = "your_api_key"

# Define the sign systems and their subcategories
sign_systems = {
    "Biological Sign Systems": {
        "Genetic Sign Systems": ["DNA", "RNA", "Protein Synthesis", "Epigenetics"],
        "Cellular Sign Systems": ["Signal Transduction", "Receptor-Ligand Interactions", "Intracellular Communication", "Intercellular Communication"],
        "Ecological Sign Systems": ["Symbiosis", "Pollination", "Seed Dispersal", "Animal Behavior"],
        "Evolutionary Sign Systems": ["Natural Selection", "Coevolution", "Speciation"]
    },
    "Human Sign Systems": {
        "Linguistic Sign Systems": ["Phonology", "Morphology", "Syntax", "Semantics", "Pragmatics"],
        "Nonverbal Sign Systems": ["Gestures", "Facial Expressions", "Body Language", "Proxemics"],
        "Cultural Sign Systems": ["Symbols", "Rituals", "Art", "Myths"],
        "Technological Sign Systems": ["Digital Communication", "Internet of Things", "Artificial Intelligence"]
    },
    "Animal Sign Systems": {
        "Vocalizations": ["Birds", "Mammals", "Amphibians", "Insects"],
        "Chemical Communication": ["Pheromones", "Scent Marking", "Alarm Signals", "Trail Markers"],
        "Visual Signals": ["Coloration", "Bioluminescence", "Postures", "Movements"],
        "Tactile Signals": ["Grooming", "Touch", "Vibrations"]
    },
    "Artificial Sign Systems": {
        "Formal Languages": ["Mathematical Symbols", "Programming Languages", "Logical Notation", "Chemical Formulae"],
        "Road Signs": ["Regulatory Signs", "Warning Signs", "Informational Signs", "Guide Signs"],
        "Maritime Signals": ["Flags", "Lights", "Sound Signals", "Buoys"],
        "Aviation Signals": ["Air Traffic Control", "Navigation Lights", "Ground Signals", "In-Flight Signals"]
    },
    "Semiotic Theories": {
        "Structural Semiotics": ["Structural Semiotics"],
        "Peircean Semiotics": ["Peircean Semiotics"],
        "Saussurean Semiotics": ["Saussurean Semiotics"],
        "Biosemiotics": ["Biosemiotics"],
        "Cognitive Semiotics": ["Cognitive Semiotics"],
        "Cultural Semiotics": ["Cultural Semiotics"],
        "Semiotic Anthropology": ["Semiotic Anthropology"],
        "Comics Semiotics": ["Comics Semiotics"],
        "Computational Semiotics": ["Computational Semiotics"],
        "Cultural and Literary Semiotics": ["Cultural and Literary Semiotics"],
        "Cybersemiotics": ["Cybersemiotics"],
        "Design Semiotics": ["Design Semiotics"],
        "Ethnosemiotics": ["Ethnosemiotics"],
        "Film Semiotics": ["Film Semiotics"],
        "Finite Semiotics": ["Finite Semiotics"],
        "Gregorian Chant Semiology": ["Gregorian Chant Semiology"],
        "Hylosemiotics": ["Hylosemiotics"],
        "Law and Semiotics": ["Law and Semiotics"],
        "Marketing Semiotics": ["Marketing Semiotics"],
        "Music Semiotics": ["Music Semiotics"],
        "Organizational Semiotics": ["Organizational Semiotics"],
        "Pictorial Semiotics": ["Pictorial Semiotics"],
        "Semiotics of Music Videos": ["Semiotics of Music Videos"],
        "Social Semiotics": ["Social Semiotics"],
        "Structuralism and Post-Structuralism": ["Structuralism and Post-Structuralism"],
        "Theatre Semiotics": ["Theatre Semiotics"],
        "Urban Semiotics": ["Urban Semiotics"],
        "Visual Semiotics": ["Visual Semiotics"],
        "Semiotics of Photography": ["Semiotics of Photography"],
        "Artificial Intelligence Semiotics": ["Artificial Intelligence Semiotics"],
        "Semiotics of Mathematics": ["Semiotics of Mathematics"]
    }
}

# Definitions corresponding to the directory structure
definitions = {
    "DNA": "DNA: The molecule that carries genetic information in all living organisms and many viruses.",
    "RNA": "RNA: A molecule involved in decoding, regulation, and expression of genes.",
    "Protein Synthesis": "Protein Synthesis: The process by which cells build proteins, involving transcription and translation.",
    "Epigenetics": "Epigenetics: The study of heritable changes in gene expression that do not involve changes to the underlying DNA sequence.",
    "Signal Transduction": "Signal Transduction: The process by which a cell responds to external signals via a series of molecular changes.",
    "Receptor-Ligand Interactions": "Receptor-Ligand Interactions: The binding of a ligand (such as a hormone or neurotransmitter) to a receptor, initiating a cellular response.",
    "Intracellular Communication": "Intracellular Communication: The communication processes that occur within a single cell.",
    "Intercellular Communication": "Intercellular Communication: The communication between different cells through signaling molecules and other mechanisms.",
    "Symbiosis": "Symbiosis: A close and often long-term interaction between two different biological species.",
    "Pollination": "Pollination: The transfer of pollen from the male structures to the female structures of plants, enabling fertilization.",
    "Seed Dispersal": "Seed Dispersal: The movement or transport of seeds away from the parent plant to reduce competition and promote species spread.",
    "Animal Behavior": "Animal Behavior: The scientific study of everything animals do, including movement, interaction, learning, and social behavior.",
    "Natural Selection": "Natural Selection: The process by which organisms better adapted to their environment tend to survive and produce more offspring.",
    "Coevolution": "Coevolution: The process by which two or more species reciprocally affect each other's evolution.",
    "Speciation": "Speciation: The formation of new and distinct species in the course of evolution.",
    "Phonology": "Phonology: The study of the sound systems of languages.",
    "Morphology": "Morphology: The study of the structure and form of words in a language.",
    "Syntax": "Syntax: The study of the rules that govern the structure of sentences.",
    "Semantics": "Semantics: The study of meaning in language.",
    "Pragmatics": "Pragmatics: The study of how context influences the interpretation of meaning in communication.",
    "Gestures": "Gestures: Movements of the body, especially the hands and arms, used to communicate or emphasize ideas or emotions.",
    "Facial Expressions": "Facial Expressions: The use of facial movements to convey emotions, intentions, or information.",
    "Body Language": "Body Language: Nonverbal communication through body movements, postures, and gestures.",
    "Proxemics": "Proxemics: The study of how people use space in communication, including personal distance and territory.",
    "Symbols": "Symbols: Objects, figures, sounds, or images that represent abstract ideas or concepts.",
    "Rituals": "Rituals: Formalized actions or series of actions performed in a prescribed order, often for ceremonial or symbolic purposes.",
    "Art": "Art: Creative visual, auditory, or performance artifacts that express imaginative, conceptual, or technical skill.",
    "Myths": "Myths: Traditional stories that embody cultural beliefs and values, often involving gods, ancestors, or heroes.",
    "Digital Communication": "Digital Communication: The exchange of information through digital devices and platforms.",
    "Internet of Things": "Internet of Things: The network of physical objects embedded with sensors and connectivity to enable communication and data exchange.",
    "Artificial Intelligence": "Artificial Intelligence: The simulation of human intelligence in machines designed to think and learn.",
    "Birds": "Bird Vocalizations: Sounds produced by birds for communication, including songs and calls.",
    "Mammals": "Mammal Vocalizations: Sounds produced by mammals for communication, including calls, grunts, and roars.",
    "Amphibians": "Amphibian Vocalizations: Sounds produced by amphibians, particularly frogs and toads, for communication.",
    "Insects": "Insect Vocalizations: Sounds produced by insects for communication, including stridulation and buzzing.",
    "Pheromones": "Pheromones: Chemicals released by an organism that affect the behavior or physiology of others of its species.",
    "Scent Marking": "Scent Marking: The use of scents to mark territory or convey information about an individual's presence or reproductive status.",
    "Alarm Signals": "Alarm Signals: Chemical or auditory signals produced by animals to warn others of danger.",
    "Trail Markers": "Trail Markers: Chemicals laid down by insects to create paths that guide others to food sources or nesting sites.",
    "Coloration": "Coloration: The use of color patterns by animals for communication, camouflage, or warning.",
    "Bioluminescence": "Bioluminescence: The production and emission of light by living organisms, often used for communication or attracting prey.",
    "Postures": "Postures: The use of body positions by animals to convey information or intentions.",
    "Movements": "Movements: Specific actions or sequences of actions performed by animals to communicate, such as mating dances or threat displays.",
    "Grooming": "Grooming: The use of touch by animals to clean or comfort each other, often serving social bonding functions.",
    "Touch": "Touch: The use of physical contact by animals to convey information or emotions.",
    "Vibrations": "Vibrations: The use of substrate-borne vibrations by animals to communicate, such as in spider web signaling or elephant ground communication.",
    "Mathematical Symbols": "Mathematical Symbols: Symbols used to represent numbers, operations, relations, and other mathematical concepts.",
    "Programming Languages": "Programming Languages: Formal languages comprising sets of instructions used to produce various kinds of output from a computer.",
    "Logical Notation": "Logical Notation: A system of symbols used to represent logical expressions and arguments.",
    "Chemical Formulae": "Chemical Formulae: Representations of chemical substances using symbols for their constituent elements and their ratios.",
    "Regulatory Signs": "Regulatory Signs: Road signs that provide information about traffic laws and regulations.",
    "Warning Signs": "Warning Signs: Road signs that alert drivers to potential hazards or changes in road conditions.",
    "Informational Signs": "Informational Signs: Road signs that provide information about routes, distances, services, and points of interest.",
    "Guide Signs": "Guide Signs: Road signs that provide directional information to help drivers navigate.",
    "Flags": "Maritime Flags: Flags used to communicate information between ships and shore or between ships at sea.",
    "Lights": "Navigation Lights: Lights used on vessels to indicate their position, heading, and status to other vessels.",
    "Sound Signals": "Sound Signals: Auditory signals, such as horns or bells, used in maritime navigation to communicate information about vessel movements and conditions.",
    "Buoys": "Buoys: Floating markers used to indicate navigational routes, hazards, and other information in waterways.",
    "Air Traffic Control": "Air Traffic Control: The system of managing aircraft movements on the ground and in the air to ensure safety and efficiency.",
    "Navigation Lights": "Aviation Navigation Lights: Lights used on aircraft to indicate position, direction, and status.",
    "Ground Signals": "Ground Signals: Visual signals used on airport runways and taxiways to guide aircraft movements.",
    "In-Flight Signals": "In-Flight Signals: Visual and auditory signals used inside the aircraft to communicate with passengers and crew.",
    "Structural Semiotics": "Structural Semiotics: The study of signs and symbols as elements of communicative systems, emphasizing their structural relationships.",
    "Peircean Semiotics": "Peircean Semiotics: A theory of signs developed by Charles Sanders Peirce, focusing on the triadic relationship between sign, object, and interpretant.",
    "Saussurean Semiotics": "Saussurean Semiotics: A theory of signs developed by Ferdinand de Saussure, emphasizing the binary relationship between the signifier and the signified.",
    "Biosemiotics": "Biosemiotics: The study of communication and sign processes in living organisms.",
    "Cognitive Semiotics": "Cognitive Semiotics: The interdisciplinary study of meaning-making processes, combining insights from semiotics, cognitive science, and linguistics.",
    "Cultural Semiotics": "Cultural Semiotics: The study of signs and symbols within cultural contexts, exploring how meaning is constructed and interpreted in cultural practices.",
    "Semiotic Anthropology": "Semiotic Anthropology: The study of human signs and symbols in social and cultural contexts.",
    "Comics Semiotics": "Comics Semiotics: The analysis of codes and signs in comics.",
    "Computational Semiotics": "Computational Semiotics: The application of semiotics in human-computer interaction and AI.",
    "Cultural and Literary Semiotics": "Cultural and Literary Semiotics: The examination of signs in literature and culture.",
    "Cybersemiotics": "Cybersemiotics: The integration of cybernetics and semiotics in a common framework.",
    "Design Semiotics": "Design Semiotics: The use of signs in product and industrial design.",
    "Ethnosemiotics": "Ethnosemiotics: The link between semiotics and ethnographic methods.",
    "Film Semiotics": "Film Semiotics: The study of signs and codes in film.",
    "Finite Semiotics": "Finite Semiotics: The semiotics of technology and its impact on human thought.",
    "Gregorian Chant Semiology": "Gregorian Chant Semiology: The semiotic analysis of Gregorian chant.",
    "Hylosemiotics": "Hylosemiotics: The understanding of meaning as inference through physical interaction.",
    "Law and Semiotics": "Law and Semiotics: The exploration of semiotics in legal contexts.",
    "Marketing Semiotics": "Marketing Semiotics: The application of semiotics to advertising and brand communication.",
    "Music Semiotics": "Music Semiotics: The study of signs in music.",
    "Organizational Semiotics": "Organizational Semiotics: The semiotic processes in organizational contexts.",
    "Pictorial Semiotics": "Pictorial Semiotics: The analysis of visual signs in art.",
    "Semiotics of Music Videos": "Semiotics of Music Videos: The semiotic analysis of popular music videos.",
    "Social Semiotics": "Social Semiotics: The study of cultural codes in social contexts.",
    "Structuralism and Post-Structuralism": "Structuralism and Post-Structuralism: The semiotic theories of structuralism and post-structuralism.",
    "Theatre Semiotics": "Theatre Semiotics: The application of semiotics to theatre studies.",
    "Urban Semiotics": "Urban Semiotics: The study of meaning in urban forms.",
    "Visual Semiotics": "Visual Semiotics: The analysis of visual signs and their meanings.",
    "Semiotics of Photography": "Semiotics of Photography: The study of symbolism in photography.",
    "Artificial Intelligence Semiotics": "Artificial Intelligence Semiotics: The semiotics of AI systems.",
    "Semiotics of Mathematics": "Semiotics of Mathematics: The study of signs in mathematics."
}

def gpt_categorization_and_signifier_chain(keyword, images=None):
    prompt = f"Categorize the following keyword or phrase into the relevant sign systems and assign weights to the influence of each sign system in its formation. Additionally, deconstruct the input into a signifier chain. The sign systems are: {list(sign_systems.keys())}. Keyword: {keyword}"
    if images:
        prompt += "\nAdditionally, consider the attached images in the categorization process."

    messages = [
        {"role": "system", "content": "You are an expert in categorizing sign systems and deconstructing signifier chains."},
        {"role": "user", "content": prompt}
    ]

    if images:
        for i, image in enumerate(images):
            messages.append({"role": "user", "content": f"Image {i+1}", "image": image})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=3000,
        temperature=0.7
    )

    return response.choices[0].message["content"].strip()

def parse_gpt_response(response):
    weights = {}
    signifier_chain = ""

    for category in sign_systems.keys():
        match = re.search(rf"{category}: (\d+)%", response)
        if match:
            weights[category] = int(match.group(1))

    signifier_chain_match = re.search(r"Signifier Chain: (.*)", response)
    if signifier_chain_match:
        signifier_chain = signifier_chain_match.group(1).strip()

    return weights, signifier_chain

def simple_categorization(keyword):
    categories = {category: 0 for category in sign_systems}
    subcategories = {category: {sub: 0 for sub in subs} for category, subs in sign_systems.items()}

    keyword_lower = keyword.lower()

    for category, subcategories_dict in sign_systems.items():
        for subcategory, terms in subcategories_dict.items():
            for term in terms:
                if term.lower() in keyword_lower:
                    categories[category] += 1
                    subcategories[category][subcategory] += 1

    return categories, subcategories

def combine_categorizations(simple_results, gpt_results):
    simple_categories, simple_subcategories = simple_results
    gpt_weights, _ = gpt_results
    combined = {key: 0 for key in sign_systems}
    combined_subcategories = {key: {sub: 0 for sub in subs} for key, subs in sign_systems.items()}

    # Combine weights for categories
    for category in combined:
        combined[category] = simple_categories.get(category, 0) + gpt_weights.get(category, 0)

    # Normalize weights for categories
    total_weight = sum(combined.values())
    if total_weight == 0:
        print("No significant sign systems found for the given keyword.")
        return
    normalized_weights = {category: (weight / total_weight) * 100 for category, weight in combined.items()}

    # Combine weights for subcategories
    for category in combined_subcategories:
        for subcategory in combined_subcategories[category]:
            combined_subcategories[category][subcategory] = simple_subcategories[category].get(subcategory, 0)

    return normalized_weights, combined_subcategories

def generate_summary(keyword, weights, subcategories):
    summary = f"Summary of the influence of sign systems on '{keyword}':\n\n"
    for category, weight in weights.items():
        summary += f"{category}: {weight:.2f}%\n"
        for subcategory, subweight in subcategories[category].items():
            summary += f"  {subcategory}: {subweight:.2f}%\n"
    return summary

def generate_output(keyword, weights, subcategories, summary, signifier_chain):
    output = f"Categorized Sign Systems and Their Influence on '{keyword}':\n\nOverview:\n"
    for category, weight in weights.items():
        output += f"{category}: {weight:.2f}%\n"
        for subcategory, subweight in subcategories[category].items():
            output += f"  {subcategory}: {subweight:.2f}%\n"
    output += "\nDetailed Descriptions:\n"
    for category, weight in weights.items():
        output += f"\n{category}: {weight:.2f}%\n"
        for subcategory in sign_systems[category]:
            for sign in sign_systems[category][subcategory]:
                output += f"  {sign}: {definitions[sign]}\n"
    output += "\nSummary:\n"
    output += summary
    output += "\n\nSignifier Chain:\n"
    output += signifier_chain
    return output

def extract_text_and_images_from_pdf(pdf_path):
    keyword = ""
    images = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            # Extract text
            keyword += page.extract_text()

    # Convert PDF pages to images
    pdf_images = convert_from_path(pdf_path)
    for i, img in enumerate(pdf_images):
        img_path = f"page_{i + 1}.png"
        img.save(img_path)
        images.append(img_path)

    return keyword, images

def split_text_into_batches(text, max_tokens_per_batch):
    words = text.split()
    batches = []
    current_batch = []

    for word in words:
        current_batch.append(word)
        if len(current_batch) >= max_tokens_per_batch:
            batches.append(' '.join(current_batch))
            current_batch = []

    if current_batch:
        batches.append(' '.join(current_batch))

    return batches

def main():
    # Check if input.pdf exists, otherwise fall back to input.txt
    input_file = "input.pdf" if os.path.exists("input.pdf") else "input.txt"

    if input_file.endswith(".pdf"):
        keyword, images = extract_text_and_images_from_pdf(input_file)
    else:
        with open(input_file, "r") as file:
            keyword = file.read().strip()
        images = None

    # Split the text into batches if necessary
    max_tokens_per_batch = 3000  # Adjust as needed
    batches = split_text_into_batches(keyword, max_tokens_per_batch)
    gpt_responses = []

    for batch in batches:
        response = gpt_categorization_and_signifier_chain(batch, images)
        gpt_responses.append(response)

    # Combine the GPT responses
    combined_gpt_response = ' '.join(gpt_responses)
    gpt_results = parse_gpt_response(combined_gpt_response)

    # Categorize using simple string matching
    simple_results = simple_categorization(keyword)

    # Combine results
    combined_weights, combined_subcategories = combine_categorizations(simple_results, gpt_results)

    # Generate summary
    summary = generate_summary(keyword, combined_weights, combined_subcategories)

    # Extract signifier chain
    _, signifier_chain = gpt_results

    # Generate output
    output = generate_output(keyword, combined_weights, combined_subcategories, summary, signifier_chain)
    with open("output.txt", "w") as f:
        f.write(output)

if __name__ == "__main__":
    main()
