# skills.md

skills:
  - name: retrieve_documents
    description: Opens and reads all 3 required policy files, and parses them into an indexed dictionary by document name and section number.
    input: File paths to the three required policy .txt documents.
    output: A nested dictionary structured as {document_name: {section_number: section_text}}.
    error_handling: Raise FileNotFoundError if any document is missing or inaccessible.

  - name: answer_question
    description: Searches the indexed documents to find the single correct answer to a user's question, completely refusing to blend rules.
    input: User's question string, and the indexed document dictionary.
    output: The single-source answer with document name + section number citation, OR the exact refusal template.
    error_handling: Return the exact verbatim refusal template if the answer requires cross-document blending, relies on hedged answers, or is simply not present.
