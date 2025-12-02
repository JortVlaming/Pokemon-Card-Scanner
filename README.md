# Pokemon Card Scanner

A simple Pokemon card recognition system using perceptual hashing. Point your camera at a Pokemon card and the system will identify the set and card number.

## Features

- **Multi-set support**: Organize cards by set in separate folders
- **Fast recognition**: Uses perceptual hashing for quick card matching
- **Simple setup**: Just add card images and run
- **No database required**: Uses lightweight JSON storage

## Quick Start

### 1. Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add Your Card Images

Create a folder structure like this:

```
cards/
  ├── evolutions/
  │   ├── 1.png
  │   ├── 2.png
  │   └── ...
  ├── base_set/
  │   ├── 1.png
  │   └── ...
```

- Each subfolder in `cards/` represents a card set
- Name your card images with their card numbers (1.png, 2.png, etc.)
- Use PNG format for best results

### 3. Run the Scanner

```bash
python3 main.py
```

The system will automatically:
- Detect if the database needs to be created or updated
- Generate hash data for any new or modified cards
- Start the card scanner

Point your camera at a card. When detected, you'll see:
- **Set**: The folder name (e.g., "evolutions")
- **Card Number**: The card number within that set

Press 'q' to quit.

## Adding New Cards

Simply add card images to the `cards/` folder structure and run the scanner - it will automatically detect and process new cards!

## Project Structure

```
Pokemon-Card-Scanner/
├── cards/              # Card images organized by set
│   └── evolutions/     # Example set
├── cardLoader.py       # Loads cards from folders
├── cardData.py         # Generates and compares card hashes
├── utils.py            # Image processing utilities
├── main.py             # Main application
└── requirements.txt    # Python dependencies
```

## How It Works

1. **Card Loading**: Scans `cards/` directory for all card images
2. **Hash Generation**: Creates perceptual hashes for each card in 4 orientations (normal, mirrored, upside-down, mirrored upside-down)
3. **Auto-Detection**: Automatically detects if database needs regeneration (missing files, new cards, or modified cards)
4. **Card Detection**: Captures camera feed, detects card edges, warps perspective
5. **Matching**: Compares captured card hash against database to find the best match

## Adding New Cards

1. Create a new folder in `cards/` (e.g., `cards/jungle/`)
2. Add numbered PNG images (1.png, 2.png, etc.)
3. Run `python3 main.py` - it will automatically detect and process the new cards!

The system automatically regenerates the database when:
- JSON files are missing
- New cards are added
- Existing cards are modified
- Card count doesn't match database

See [ADDING_CARDS.md](ADDING_CARDS.md) for detailed instructions.

## Camera Setup

- **Video source 0**: Built-in webcam (default)
- **Video source 1**: External camera/phone

Edit `main.py` line 10 to change the camera source:
```python
cam = cv2.VideoCapture(0)  # Change 0 to 1 for external camera
```

## Troubleshooting

**No cards detected?**
- Ensure good lighting
- Hold card flat and steady
- Make sure the entire card is visible
- Try adjusting the camera angle

**Wrong card detected?**
- The hash cutoff value (default: 18) may need adjustment
- Edit `cardData.py` line 118 to change the cutoff value

## Requirements

- Python 3.7+
- OpenCV
- NumPy
- Pillow
- ImageHash

## License

See LICENSE file for details.
