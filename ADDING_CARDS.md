# Adding New Card Images

## Folder Structure

To add new card images, organize them in the following structure:

```
cards/
  ├── evolutions/
  │   ├── 1.png
  │   ├── 2.png
  │   ├── 3.png
  │   └── ...
  ├── base_set/
  │   ├── 1.png
  │   ├── 2.png
  │   └── ...
  └── jungle/
      ├── 1.png
      ├── 2.png
      └── ...
```

## Steps to Add New Cards

1. **Create the `cards/` directory** in your project root if it doesn't exist

2. **Create a folder for each card set** (e.g., `evolutions`, `base_set`, `jungle`)

3. **Add card images** as numbered PNG files (1.png, 2.png, 3.png, etc.)

4. **Run the scanner**:
   ```bash
   python3 main.py
   ```
   The system will automatically detect new cards and regenerate the database!

## Automatic Database Updates

The system automatically regenerates the database when:
- JSON files don't exist
- You add new cards to any set folder
- You modify existing card images
- The number of cards doesn't match the database

You never need to manually trigger database regeneration - just add your cards and run!

## Notes

- Card images should be PNG format
- Number your cards sequentially (1.png, 2.png, 3.png, etc.)
- Each folder name becomes the "set name" displayed when a card is detected
- The system automatically generates perceptual hashes for card matching
- Database updates happen automatically - no manual intervention needed!
