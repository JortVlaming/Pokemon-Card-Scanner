import os
import numpy as np
import imagehash
from PIL import Image, ImageOps


class CardLoader:
    """
    Dynamically loads card images from a folder structure organized by sets.
    
    Expected folder structure:
    cards/
      ├── set1/
      │   ├── 1.png
      │   ├── 2.png
      │   └── ...
      ├── set2/
      │   ├── 1.png
      │   └── ...
    """
    
    def __init__(self, cards_root='cards'):
        """
        Initialize the CardLoader.
        
        Args:
            cards_root: Root directory containing set folders
        """
        self.cards_root = cards_root
        self.cards = []  # List of card dictionaries with metadata
        self.hashes = []  # List of hash arrays (normal orientation)
        self.hashesmir = []  # List of hash arrays (mirrored)
        self.hashesud = []  # List of hash arrays (upside down)
        self.hashesudmir = []  # List of hash arrays (upside down mirrored)
        
        if os.path.exists(cards_root):
            self._load_all_cards()
    
    def _load_all_cards(self):
        """Scan the cards directory and load all card images."""
        if not os.path.exists(self.cards_root):
            print(f"Warning: Cards directory '{self.cards_root}' not found.")
            return
        
        # Get all subdirectories (sets)
        sets = [d for d in os.listdir(self.cards_root) 
                if os.path.isdir(os.path.join(self.cards_root, d)) and not d.startswith('.')]
        
        if not sets:
            print(f"Warning: No set folders found in '{self.cards_root}'")
            return
        
        sets.sort()  # Sort for consistent ordering
        
        global_card_id = 1
        
        for set_name in sets:
            set_path = os.path.join(self.cards_root, set_name)
            
            # Get all PNG files in the set folder
            card_files = [f for f in os.listdir(set_path) 
                         if f.lower().endswith('.png')]
            
            # Sort by numeric value (assuming filenames like 1.png, 2.png, etc.)
            card_files.sort(key=lambda x: int(os.path.splitext(x)[0]) if os.path.splitext(x)[0].isdigit() else 0)
            
            for card_file in card_files:
                card_path = os.path.join(set_path, card_file)
                card_number_in_set = os.path.splitext(card_file)[0]
                
                try:
                    # Load image and generate hashes
                    img = Image.open(card_path)
                    
                    # Store card metadata
                    self.cards.append({
                        'global_id': global_card_id,
                        'set_name': set_name,
                        'card_number_in_set': card_number_in_set,
                        'file_path': card_path
                    })
                    
                    # Generate hashes for all orientations
                    self.hashes.append(self._get_hashes_for_image(img, 'hash'))
                    self.hashesmir.append(self._get_hashes_for_image(img, 'hashmir'))
                    self.hashesud.append(self._get_hashes_for_image(img, 'hashud'))
                    self.hashesudmir.append(self._get_hashes_for_image(img, 'hashudmir'))
                    
                    global_card_id += 1
                    
                except Exception as e:
                    print(f"Error loading {card_path}: {e}")
        
        print(f"Loaded {len(self.cards)} cards from {len(sets)} sets")
    
    def _get_hashes_for_image(self, img, orientation_type):
        """
        Generate 4 different hash types for an image in a specific orientation.
        
        Args:
            img: PIL Image object
            orientation_type: 'hash', 'hashmir', 'hashud', or 'hashudmir'
            
        Returns:
            Array of 4 hash strings [average_hash, whash, phash, dhash]
        """
        # Apply orientation transformation
        if orientation_type == 'hash':
            oriented_img = img
        elif orientation_type == 'hashmir':
            oriented_img = ImageOps.mirror(img)
        elif orientation_type == 'hashud':
            oriented_img = ImageOps.flip(img)
        elif orientation_type == 'hashudmir':
            oriented_img = ImageOps.flip(ImageOps.mirror(img))
        else:
            oriented_img = img
        
        # Generate 4 different hash types
        return [
            str(imagehash.average_hash(oriented_img)),
            str(imagehash.whash(oriented_img)),
            str(imagehash.phash(oriented_img)),
            str(imagehash.dhash(oriented_img))
        ]
    
    def get_card_count(self):
        """Return the total number of cards loaded."""
        return len(self.cards)
    
    def get_card_metadata(self, global_id):
        """
        Get metadata for a specific card by its global ID.
        
        Args:
            global_id: Global card ID (1-indexed)
            
        Returns:
            Dictionary with card metadata or None if not found
        """
        if 1 <= global_id <= len(self.cards):
            return self.cards[global_id - 1]
        return None
