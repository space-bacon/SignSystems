from openai import OpenAI

client = OpenAI(api_key="your_api_key")
import os
import zipfile
import re
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image

# Set your OpenAI API key

# Define the sign systems and their subcategories
sign_systems = {
    "Biological_Sign_Systems": {
        "Genetic_Sign_Systems": ["DNA", "RNA", "Protein Synthesis", "Epigenetics"],
        "Cellular_Sign_Systems": ["Signal Transduction", "Receptor-Ligand Interactions", "Intracellular Communication", "Intercellular Communication"],
        "Ecological_Sign_Systems": ["Symbiosis", "Pollination", "Seed Dispersal", "Animal Behavior"],
        "Evolutionary_Sign_Systems": ["Natural Selection", "Coevolution", "Speciation"]
    },
    "Human_Sign_Systems": {
        "Linguistic_Sign_Systems": ["Phonology", "Morphology", "Syntax", "Semantics", "Pragmatics"],
        "Nonverbal_Sign_Systems": ["Gestures", "Facial Expressions", "Body Language", "Proxemics"],
        "Cultural_Sign_Systems": ["Symbols", "Rituals", "Art", "Myths"],
        "Technological_Sign_Systems": ["Digital Communication", "Internet of Things", "Artificial Intelligence"]
    },
    "Animal_Sign_Systems": {
        "Vocalizations": ["Birds", "Mammals", "Amphibians", "Insects"],
        "Chemical_Communication": ["Pheromones", "Scent Marking", "Alarm Signals", "Trail Markers"],
        "Visual_Signals": ["Coloration", "Bioluminescence", "Postures", "Movements"],
        "Tactile_Signals": ["Grooming", "Touch", "Vibrations"]
    },
    "Artificial_Sign_Systems": {
        "Formal_Languages": ["Mathematical Symbols", "Programming Languages", "Logical Notation", "Chemical Formulae"],
        "Road_Signs": ["Regulatory Signs", "Warning Signs", "Informational Signs", "Guide Signs"],
        "Maritime_Signals": ["Flags", "Lights", "Sound Signals", "Buoys"],
        "Aviation_Signals": ["Air Traffic Control", "Navigation Lights", "Ground Signals", "In-Flight Signals"]
    },
    "Semiotic_Theories": {
        "Structural_Semiotics": ["Structural Semiotics"],
        "Peircean_Semiotics": ["Peircean Semiotics"],
        "Saussurean_Semiotics": ["Saussurean Semiotics"],
        "Biosemiotics": ["Biosemiotics"],
        "Cognitive_Semiotics": ["Cognitive Semiotics"],
        "Cultural_Semiotics": ["Cultural Semiotics"]
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
    "Cultural Semiotics": "Cultural Semiotics: The study of signs and symbols within cultural contexts, exploring how meaning is constructed and interpreted in cultural practices."
}

def gpt_categorization(keyword, images=None):
    prompt = f"Categorize the following keyword or phrase into the relevant sign systems and assign weights to the influence of each sign system in its formation. The sign systems are: {list(sign_systems.keys())}. Keyword: {keyword}"
    if images:
        prompt += "\nAdditionally, consider the attached images in the categorization process."

    messages = [
        {"role": "system", "content": "You are an expert in categorizing sign systems."},
        {"role": "user", "content": prompt}
    ]

    if images:
        for i, image in enumerate(images):
            messages.append({"role": "user", "content": f"Image {i+1}", "image": image})

    response = client.chat.completions.create(model="gpt-4",
    messages=messages,
    max_tokens=300,
    temperature=0.7)

    return response.choices[0].message.content.strip()

def parse_gpt_response(response):
    weights = {}
    for category in sign_systems.keys():
        match = re.search(rf"{category}: (\d+)%", response)
        if match:
            weights[category] = int(match.group(1))
    return weights

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
    combined = {key: 0 for key in sign_systems}
    combined_subcategories = {key: {sub: 0 for sub in subs} for key, subs in sign_systems.items()}

    # Combine weights for categories
    for category in combined:
        combined[category] = simple_categories.get(category, 0) + gpt_results.get(category, 0)

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

def generate_output(keyword, weights, subcategories, summary):
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
    return output

def create_project_structure():
    base_dir = "Sign_Systems"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    for main_category in sign_systems:
        main_dir = os.path.join(base_dir, main_category)
        os.makedirs(main_dir, exist_ok=True)
        for sub_category in sign_systems[main_category]:
            sub_dir = os.path.join(main_dir, sub_category.replace(" ", "_"))
            os.makedirs(sub_dir, exist_ok=True)
            for sign in sign_systems[main_category][sub_category]:
                sign_dir = os.path.join(sub_dir, sign.replace(" ", "_"))
                os.makedirs(sign_dir, exist_ok=True)
                with open(os.path.join(sign_dir, "readme.md"), "w") as f:
                    f.write(definitions[sign])

def zip_project_structure():
    with zipfile.ZipFile('Sign_Systems_Project.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('Sign_Systems'):
            for file in files:
                zipf.write(os.path.join(root, file))

def create_readme():
    readme_content = """
# Sign Systems Categorization Project

## Overview

This project categorizes a given keyword or phrase into various sign systems and subcategories to analyze the influence of each sign system. The project uses both simple string matching and GPT-4 to provide an in-depth analysis and detailed descriptions.

## Sign Systems and Subcategories

The project categorizes the input into the following sign systems and their respective subcategories:

### Biological Sign Systems
- Genetic Sign Systems
- Cellular Sign Systems
- Ecological Sign Systems
- Evolutionary Sign Systems

### Human Sign Systems
- Linguistic Sign Systems
- Nonverbal Sign Systems
- Cultural Sign Systems
- Technological Sign Systems

### Animal Sign Systems
- Vocalizations
- Chemical Communication
- Visual Signals
- Tactile Signals

### Artificial Sign Systems
- Formal Languages
- Road Signs
- Maritime Signals
- Aviation Signals

### Semiotic Theories
- Structural Semiotics
- Peircean Semiotics
- Saussurean Semiotics
- Biosemiotics
- Cognitive Semiotics
- Cultural Semiotics

## Process

1. **Input**: The input keyword or phrase is read from `input.txt`.
2. **Categorization**: The keyword is categorized using:
   - Simple string matching
   - GPT-4 API
3. **Combination**: The results from both methods are combined and normalized.
4. **Output**: An overview and detailed descriptions are generated and saved to `output.txt`.
5. **Project Structure**: The categorized sign systems are organized into directories with `readme.md` files containing definitions.
6. **Zip Archive**: The project structure is zipped into `Sign_Systems_Project.zip`.

## Usage

1. Place the keyword or phrase in `input.txt`.
2. Run the script.
3. The results will be printed to the console and saved in `output.txt`.
4. The project structure will be created and zipped.

## Requirements

- Python 3
- `openai` package
- GPT-4 API key

## Note

Ensure you have the `openai` package installed and a valid API key set in the script.

    """
    with open("readme.md", "w") as f:
        f.write(readme_content)

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
        response = gpt_categorization(batch, images)
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

    # Generate output
    output = generate_output(keyword, combined_weights, combined_subcategories, summary)
    with open("output.txt", "w") as f:
        f.write(output)

    # Create project structure
    create_project_structure()

    # Create zip archive
    zip_project_structure()

    # Create readme file
    create_readme()

if __name__ == "__main__":
    main()
