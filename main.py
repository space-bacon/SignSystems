from openai import OpenAI

client = OpenAI(api_key="your_api_key")
import os
import re
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

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

def gpt_generate_relational_definition(category, subcategory, keyword):
    prompt = f"Explain how the concept '{subcategory}' from '{category}' relates to the following input: {keyword}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in sign systems and semiotics."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

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
            with open(image, "rb") as img_file:
                messages.append({"role": "user", "content": f"Image {i+1}", "image": img_file.read()})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=3000,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

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
        if weight > 0:
            output += f"\n{category}: {weight:.2f}%\n"
            for subcategory in sign_systems[category]:
                if subcategories[category][subcategory] > 0:
                    relational_definition = gpt_generate_relational_definition(category, subcategory, keyword)
                    output += f"  {subcategory}: {relational_definition}\n"
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

def extract_text_from_image(image_path):
    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(Image.open(image_path))
    return text

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
    input_file = "input.pdf" if os.path.exists("input.pdf") else "input.txt"
    image_file = "/mnt/data/IMG_3495.png"

    if input_file.endswith(".pdf"):
        keyword, images = extract_text_and_images_from_pdf(input_file)
    elif input_file.endswith(".txt"):
        with open(input_file, "r") as file:
            keyword = file.read().strip()
        images = None
    elif image_file.endswith(".png"):
        keyword = extract_text_from_image(image_file)
        images = [image_file]

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
