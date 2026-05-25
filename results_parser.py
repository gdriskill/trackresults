from dataclasses import dataclass
import re
import PyPDF2
from result import Result

class ResultsParser:
    """Parses the results page for a given track meet and extracts relevant information."""
    
    def __init__(self, filename):
        self.filename = filename

    def is_page_header(self, line):
        patterns = [
            r"Hy-Tek's MEET MANAGER",
            r"Page \\d+",
            r"\\d{1,2}:\\d{2} (AM|PM)"
        ]
        return any(re.search(p, line) for p in patterns)

    def parse_results(self):
        # Creating a pdf file object
        pdfFileObj = open(self.filename, 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        pages = len(pdfReader.pages)
        pageObjs = [pdfReader.pages[i] for i in range(pages)]
        full_text = [i.extract_text().split("\n") for i in pageObjs]
        full_text = [item for sublist in full_text for item in sublist]

        results = []
        current_event = None
        in_results_section = False
        i = 0
        while i < len(full_text):
            line = full_text[i]
            # detect first line of page header and skip next 3 lines as well (page header is 4 lines total)
            if self.is_page_header(line):
                print(f"Detected page header at line {i}: {line}")
                i += 4
                continue
            # Detect event header for start of results section
            event_match = re.match(r"Event\s+\d+\s+(.+)", line)
            if event_match:
                print(f"Detected event header at line {i}: {line}")
                lookahead1 = full_text[i+1] if i+1 < len(full_text) else ""
                lookahead3 = full_text[i+3] if i+3 < len(full_text) else ""
                if lookahead1.startswith("===") and lookahead3.startswith("==="):
                    print(f"Confirmed event header at line {i}: {line}")
                    current_event = event_match.group(1).strip()
                    in_results_section = False
                    i += 4
                continue
            # End of results section
            if in_results_section and line.startswith('===='):
                print(f"Detected end of results section at line {i}: {line}")
                in_results_section = False
                current_event = None
            # Detect start of finals results section
            if current_event and line.strip().startswith('Finals'):
                print(f"Detected start of results section at line {i}: {line}")
                in_results_section = True
                i += 1
                continue
            # Parse result lines
            if in_results_section and not line.startswith("...Event"):  # handle end case where results section is split across pages and "Event" header is repeated with "..." prefix
                try:
                    result = Result(line, current_event)
                    results.append(result)
                except ValueError as e:
                    print(f"Error parsing line {i}: {line}")
                    print(f"ValueError: {e}")
            i += 1
        pdfFileObj.close()
        return results

    def print_results(self, results):
        for result in results:
            print(result)