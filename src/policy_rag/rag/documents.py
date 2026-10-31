"""Section 1a: the source documents."""
from pathlib import Path
from policy_rag.rag.config import DATA_DIR

# POLICY_DOCUMENTS = [
#     {
#         "id": "policy_001",
#         "title": "Home Office Equipment Reimbursement",
#         "content": "Employees working from home may claim up to $500 per year for office equipment including desks, chairs, monitors, and computer accessories. Receipts must be submitted within 30 days of purchase. This policy applies to full-time remote workers only. The equipment must be used primarily for work purposes and should be ergonomic and suitable for a professional home office environment.",
#         "category": "reimbursement",
#     },
#     {
#         "id": "policy_002",
#         "title": "Travel Expense Guidelines",
#         "content": "Business travel expenses are reimbursable when pre-approved by your manager. Meals are covered up to $50 per day, hotel stays up to $200 per night. All receipts must be submitted within 14 days of return. International travel requires additional approval from the department head. Travel insurance is mandatory for all business trips exceeding 7 days.",
#         "category": "travel",
#     },
#     {
#         "id": "policy_003",
#         "title": "Remote Work Furniture Policy",
#         "content": "Remote employees may purchase ergonomic furniture for their home office setup. This includes standing desks, ergonomic chairs, and monitor arms. Maximum reimbursement is $300 per item with manager approval required. All furniture must meet ergonomic standards and be purchased from approved vendors. Receipts must be submitted within 45 days of purchase.",
#         "category": "reimbursement",
#     },
#     {
#         "id": "policy_004",
#         "title": "Equipment and Supplies Reimbursement",
#         "content": "Work-related equipment and supplies purchased for home office use are eligible for reimbursement. This covers laptops, monitors, keyboards, mice, and other computer peripherals. Submit expense reports with receipts for approval. Equipment must be used for work purposes and should be compatible with company systems. Annual limit is $1000 per employee.",
#         "category": "reimbursement",
#     },
#     {
#         "id": "policy_005",
#         "title": "Vacation and PTO Policy",
#         "content": "Full-time employees accrue 15 days of paid time off per year. Vacation requests must be submitted at least 2 weeks in advance. Unused PTO does not roll over to the next year. Emergency leave can be taken with manager approval. Sick leave is separate from vacation time and does not count against PTO balance.",
#         "category": "benefits",
#     },
# ]

def load_documents(data_dir: Path = DATA_DIR):
    files = sorted(Path(data_dir).rglob("*.md"))
    if not files:
        raise FileNotFoundError(f"No Files Found In: {data_dir}")

    documents = []
    for file in files:
        # print(f"{file}\n")

        text = file.read_text(encoding="utf-8").strip()
        if not text:
            continue

        relative_path = file.relative_to(data_dir)

        title = next((line.lstrip("#") for line in text.splitlines() if line.startswith("# ")),
                     file.stem.replace("-"," ").replace("_"," ").title())

        documents.append({
            "id": relative_path.with_suffix("").as_posix().replace("/","_"),
            "title": title,
            "content": text,
            "category": relative_path.parent.name or "general"
        })

    # print(f"\n{documents}")

    return documents
    
load_documents()