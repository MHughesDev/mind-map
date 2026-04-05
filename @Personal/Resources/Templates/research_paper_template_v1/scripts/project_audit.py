from pathlib import Path

status = Path("docs/PROJECT_STATUS.md")
missing = Path("docs/MISSING_INPUTS.md")
build_status = Path("docs/BUILD_STATUS.md")
pdf_review = Path("docs/PDF_REVIEW.md")
main_tex = Path("paper/main.tex")
main_pdf = Path("paper/main.pdf")

def preview(path, n=20):
    if not path.exists():
        return f"{path} missing"
    lines = path.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[:n])

def main():
    print("=== PROJECT AUDIT ===")
    print("\n--- paper/main.tex present ---")
    print(main_tex.exists())
    print("\n--- paper/main.pdf present ---")
    print(main_pdf.exists())
    print("\n--- docs/PROJECT_STATUS.md preview ---")
    print(preview(status))
    print("\n--- docs/MISSING_INPUTS.md preview ---")
    print(preview(missing))
    print("\n--- docs/BUILD_STATUS.md preview ---")
    print(preview(build_status))
    print("\n--- docs/PDF_REVIEW.md preview ---")
    print(preview(pdf_review))

if __name__ == "__main__":
    main()
