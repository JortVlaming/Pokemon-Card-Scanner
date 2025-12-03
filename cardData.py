import json
import os
import imagehash
import numpy as np


# Checks if database needs to be regenerated
def needsDatabaseRegeneration():
    """
    Check if the database JSON files need to be regenerated.
    Returns True if:
    - JSON files don't exist
    - cards/ folder has different number of cards than JSON
    - cards/ folder is newer than JSON files
    """
    # Check if JSON files exist
    if not os.path.exists('evolutions_set.json') or not os.path.exists('evolutions_cards.json'):
        return True
    
    # Count cards in cards/ folder
    import cardLoader
    loader = cardLoader.CardLoader('cards')
    card_count = loader.get_card_count()
    
    if card_count == 0:
        return False  # No cards to process
    
    # Check if JSON has same number of cards
    try:
        with open('evolutions_cards.json', 'r') as f:
            cards_data = json.load(f)
            if len(cards_data) != card_count:
                return True
    except (json.JSONDecodeError, KeyError):
        return True
    
    # Check if cards/ folder is newer than JSON files
    try:
        json_mtime = os.path.getmtime('evolutions_cards.json')
        cards_dir = 'cards'
        
        # Check all subdirectories in cards/
        for set_dir in os.listdir(cards_dir):
            set_path = os.path.join(cards_dir, set_dir)
            if os.path.isdir(set_path) and not set_dir.startswith('.'):
                # Check if any PNG file is newer than JSON
                for file in os.listdir(set_path):
                    if file.lower().endswith('.png'):
                        file_path = os.path.join(set_path, file)
                        if os.path.getmtime(file_path) > json_mtime:
                            return True
    except (OSError, FileNotFoundError):
        return True
    
    return False


# Creates JSON files for card data
def createDatabase():
    print("Creating JSON data files...")
    
    # Use CardLoader to scan cards/ directory
    import cardLoader
    loader = cardLoader.CardLoader('cards')
    
    if loader.get_card_count() == 0:
        print("ERROR: No cards found in 'cards/' folder!")
        print("Please add card images to cards/set_name/ folders")
        return
    
    print(f"Loaded {loader.get_card_count()} cards from card folders")
    
    # Create card set data
    evolutions_set_data = []
    evolutions_cards_data = []
    
    for i in range(loader.get_card_count()):
        card_meta = loader.cards[i]
        
        evolutions_set_data.append({
            'cardnumber': card_meta['global_id'],
            'set_name': card_meta['set_name'],
            'card_number_in_set': card_meta['card_number_in_set']
        })
        
        evolutions_cards_data.append({
            'cardnumber': card_meta['global_id'],
            'set_name': card_meta['set_name'],
            'card_number_in_set': card_meta['card_number_in_set'],
            'avghashes': loader.hashes[i][0],
            'avghashesmir': loader.hashesmir[i][0],
            'avghashesud': loader.hashesud[i][0],
            'avghashesudmir': loader.hashesudmir[i][0],
            'whashes': loader.hashes[i][1],
            'whashesmir': loader.hashesmir[i][1],
            'whashesud': loader.hashesud[i][1],
            'whashesudmir': loader.hashesudmir[i][1],
            'phashes': loader.hashes[i][2],
            'phashesmir': loader.hashesmir[i][2],
            'phashesud': loader.hashesud[i][2],
            'phashesudmir': loader.hashesudmir[i][2],
            'dhashes': loader.hashes[i][3],
            'dhashesmir': loader.hashesmir[i][3],
            'dhashesud': loader.hashesud[i][3],
            'dhashesudmir': loader.hashesudmir[i][3]
        })
    
    # Write to JSON files
    with open('evolutions_set.json', 'w') as f:
        json.dump(evolutions_set_data, f, indent=2)
    
    with open('evolutions_cards.json', 'w') as f:
        json.dump(evolutions_cards_data, f, indent=2)
    
    print("JSON data files created successfully!")
    print("- evolutions_set.json")
    print("- evolutions_cards.json")





# Returns a dictionary with the matching card's set and number if found
# If no matching card is found, it returns None
def compareCards(hashes):
    cutoff = 22  # Arbitrarily set cutoff value; was found through testing
    
    # Load JSON data files
    if not os.path.exists('evolutions_cards.json'):
        print("Error: JSON data files not found. Please run with isFirst=True to create them.")
        return None
    
    with open('evolutions_cards.json', 'r') as f:
        evolutions_cards = json.load(f)
    
    with open('evolutions_set.json', 'r') as f:
        evolutions_set = json.load(f)

    # Create arrays of size=4 that store hash differences for each orientation
    avghashesDists = np.zeros(4)
    whashesDists = np.zeros(4)
    phashesDists = np.zeros(4)
    dhashesDists = np.zeros(4)

    maxHashDists = []  # An array that will store the maximum of the minimum hash difference for each card

    for card in evolutions_cards:  # Loop through each card
        # Get the hash values for this card
        avghash1 = card['avghashes']
        avghash2 = card['avghashesmir']
        avghash3 = card['avghashesud']
        avghash4 = card['avghashesudmir']
        
        whash1 = card['whashes']
        whash2 = card['whashesmir']
        whash3 = card['whashesud']
        whash4 = card['whashesudmir']
        
        phash1 = card['phashes']
        phash2 = card['phashesmir']
        phash3 = card['phashesud']
        phash4 = card['phashesudmir']
        
        dhash1 = card['dhashes']
        dhash2 = card['dhashesmir']
        dhash3 = card['dhashesud']
        dhash4 = card['dhashesudmir']

        # Convert each hash from a String to a hash and find the distance from the scanned image
        avghashesDists[0] = hashes[0] - imagehash.hex_to_hash(avghash1)
        avghashesDists[1] = hashes[0] - imagehash.hex_to_hash(avghash2)
        avghashesDists[2] = hashes[0] - imagehash.hex_to_hash(avghash3)
        avghashesDists[3] = hashes[0] - imagehash.hex_to_hash(avghash4)

        whashesDists[0] = hashes[1] - imagehash.hex_to_hash(whash1)
        whashesDists[1] = hashes[1] - imagehash.hex_to_hash(whash2)
        whashesDists[2] = hashes[1] - imagehash.hex_to_hash(whash3)
        whashesDists[3] = hashes[1] - imagehash.hex_to_hash(whash4)

        phashesDists[0] = hashes[2] - imagehash.hex_to_hash(phash1)
        phashesDists[1] = hashes[2] - imagehash.hex_to_hash(phash2)
        phashesDists[2] = hashes[2] - imagehash.hex_to_hash(phash3)
        phashesDists[3] = hashes[2] - imagehash.hex_to_hash(phash4)

        dhashesDists[0] = hashes[3] - imagehash.hex_to_hash(dhash1)
        dhashesDists[1] = hashes[3] - imagehash.hex_to_hash(dhash2)
        dhashesDists[2] = hashes[3] - imagehash.hex_to_hash(dhash3)
        dhashesDists[3] = hashes[3] - imagehash.hex_to_hash(dhash4)

        # Find the minimum of each hashing method
        hashDistances = [min(avghashesDists), min(whashesDists), min(phashesDists), min(dhashesDists)]
        maxHashDists.append(max(hashDistances))

    print(min(maxHashDists))
    if min(maxHashDists) < cutoff:  # If the smallest hash distance is less than the cutoff, we have found our card
        minCardNum = maxHashDists.index(min(maxHashDists)) + 1  # Find the card number of the card

        # Get card data from evolutions_set
        card_data = next((card for card in evolutions_set if card['cardnumber'] == minCardNum), None)
        if not card_data:
            return None
        
        set_name = card_data.get('set_name', 'Unknown')
        card_number_in_set = card_data.get('card_number_in_set', 'Unknown')

        # Return simple dictionary with just set and card number
        return {
            'Card Number': minCardNum,
            'Set Name': set_name,
            'Card Number In Set': card_number_in_set
        }
    return None
