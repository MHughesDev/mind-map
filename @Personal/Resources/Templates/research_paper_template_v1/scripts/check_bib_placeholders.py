from pathlib import Path

BIB = Path("paper/bib/references.bib")
TOKENS = ["PLACEHOLDER", "Incomplete citation metadata", "@misc{placeholder_key"]

def main():
    if not BIB.exists():
        print("Bibliography file not found.")
        return
    text = BIB.read_text(encoding="utf-8")
    hits = [token for token in TOKENS if token in text]
    if hits:
        print("Bibliography contains placeholder content:")
        for token in hits:
            print("-", token)
    else:
        print("No obvious bibliography placeholders found.")

if __name__ == "__main__":
    main()
