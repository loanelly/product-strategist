# New material for decision rechecks

Place only authorized, non-sensitive UTF-8 text files here. On opening the
Cursor workspace or editing an incoming file, the project hook runs
`recheck_decisions.py`; after importing files outside Cursor, run the script
manually. Supported formats are `.csv`, `.htm`, `.html`, `.json`, `.md`,
`.txt`, and `.xml`. The script flags source-ID or watch-term matches for human
and agent review; a match is not proof that a decision is obsolete. Do not
place personal data, confidential documents, secrets, or binary files here.
