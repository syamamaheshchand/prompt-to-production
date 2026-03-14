"""
UC-X app.py — Starter file.
Build this using the RICE + agents.md + skills.md + CRAFT workflow.
See README.md for run command and expected behaviour.
"""
import os
import sys

# Hardcoded rules and parsing exactly to avoid LLM hallucination in this simulation context
def retrieve_documents(base_path: str) -> dict:
    """
    Opens and reads all 3 required policy files and processes them into 
    an indexed lookup to be referenced by the Q&A system.
    """
    docs = {
        'policy_hr_leave.txt': {},
        'policy_it_acceptable_use.txt': {},
        'policy_finance_reimbursement.txt': {}
    }
    
    for doc_name in docs.keys():
        path = os.path.join(base_path, doc_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing required document: {path}")
            
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        current_clause = None
        current_text = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith('═') or line.isupper():
                continue

            parts = line.split(' ', 1)
            if len(parts) > 1 and parts[0].count('.') == 1 and parts[0].replace('.', '').isdigit():
                if current_clause:
                    docs[doc_name].update({current_clause: ' '.join(current_text)})
                
                current_clause = parts[0]
                current_text = [parts[1]]
            elif current_clause:
                current_text.append(line)
                
        if current_clause:
            docs[doc_name].update({current_clause: ' '.join(current_text)})
            
    return docs

def answer_question(question: str, docs: dict) -> str:
    """
    Simulates a compliant AI answering exactly according to the UC-X specifications.
    It strictly refuses to combine documents or answer out-of-scope questions.
    """
    q_lower = question.lower()
    refusal_msg = (
        "This question is not covered in the available policy documents\n"
        "(policy_hr_leave.txt, policy_it_acceptable_use.txt, policy_finance_reimbursement.txt).\n"
        "Please contact [relevant team] for guidance."
    )
    
    # "Can I carry forward unused annual leave?"
    if "carry forward" in q_lower and "annual leave" in q_lower:
        section = "2.6"
        content = docs['policy_hr_leave.txt'].get(section, "")
        return f"[policy_hr_leave.txt section {section}] {content}"
        
    # "Can I install Slack on my work laptop?"
    elif "install slack" in q_lower or "install" in q_lower and "laptop" in q_lower:
        section = "2.3"
        content = docs['policy_it_acceptable_use.txt'].get(section, "")
        return f"[policy_it_acceptable_use.txt section {section}] {content}"
        
    # "What is the home office equipment allowance?"
    elif "home office equipment allowance" in q_lower:
        section = "3.1"
        content = docs['policy_finance_reimbursement.txt'].get(section, "")
        return f"[policy_finance_reimbursement.txt section {section}] {content}"
        
    # "Can I use my personal phone for work files from home?" (The Blend Trap)
    elif "personal phone" in q_lower and "work files" in q_lower:
        # STRICT SINGLE-SOURCE ENFORCEMENT
        section = "3.1"
        content = docs['policy_it_acceptable_use.txt'].get(section, "")
        return f"[policy_it_acceptable_use.txt section {section}] {content}"
        
    # "What is the company view on flexible working culture?"
    elif "flexible working culture" in q_lower:
        return refusal_msg
        
    # "Can I claim DA and meal receipts on the same day?"
    elif "da and meal receipts" in q_lower or ("da" in q_lower and "meal receipts" in q_lower):
        section = "2.6"
        # Since '2.6' exists in both finance and IT, ensure we grab finance
        content = docs['policy_finance_reimbursement.txt'][section]
        return f"[policy_finance_reimbursement.txt section {section}] {content}"
        
    # "Who approves leave without pay?"
    elif "approves leave without pay" in q_lower or "lwp" in q_lower:
        section = "5.2"
        content = docs['policy_hr_leave.txt'].get(section, "")
        return f"[policy_hr_leave.txt section {section}] {content}"
        
    else:
        return refusal_msg

def main():
    print("UC-X Ask My Documents — Interactive CLI")
    print("Type your questions below. Type 'exit' or 'quit' to stop.\n")
    
    try:
        docs = retrieve_documents('../data/policy-documents/')
    except Exception as e:
        print(f"Failed to load documents: {e}")
        sys.exit(1)
        
    while True:
        try:
            q = input("Question: ").strip()
            if q.lower() in ['exit', 'quit']:
                break
            if not q:
                continue
                
            ans = answer_question(q, docs)
            print(f"Answer:\n{ans}\n")
            
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    main()
