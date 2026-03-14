# skills.md

skills:
  - name: retrieve_policy
    description: Loads a structured .txt policy file and returns the extracted content as structured numbered sections to prevent omission.
    input: File path to the .txt policy document.
    output: A dictionary or object mapping clause numbers to their exact text.
    error_handling: If a clause cannot be parsed or if the file format is unrecognizable, raise a ValueError and refuse to process the document.

  - name: summarize_policy
    description: Takes structured clauses and produces a compliant summary that explicitly preserves all multi-condition rules without scope bleed.
    input: A dictionary of extracted policy clauses.
    output: A single string containing the compliant summary with explicit clause references.
    error_handling: If any clause requires assumption to summarize, output the clause verbatim along with a [VERBATIM] flag.
