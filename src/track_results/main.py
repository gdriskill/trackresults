import sys
import os
from track_results.results_parser import ResultsParser

"""Main entry point for track_results."""

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Parse track meet PDFs and filter results by team.")
    parser.add_argument("pdf_dir", help="Directory containing PDF files")
    parser.add_argument("team_name", help="Team name to filter results")
    parser.add_argument("--outdir", default="results_output", help="Directory to write output files")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    all_results = []
    # Parse each PDF in the directory
    for fname in os.listdir(args.pdf_dir):
        if fname.lower().endswith(".pdf"):
            pdf_path = os.path.join(args.pdf_dir, fname)
            parser = ResultsParser(pdf_path)
            results = parser.parse_results()
            all_results.extend(results)
    # Filter by team
    team_results = [r for r in all_results if args.team_name.lower() in r.team.lower()]
    # Results where needs_award() is true
    award_results = [r for r in team_results if hasattr(r, 'needs_award') and r.needs_award()]
    # Write all team results
    with open(os.path.join(args.outdir, f"{args.team_name}_all_results.txt"), "w", encoding="utf-8") as f:
        for r in team_results:
            f.write(str(r) + "\n")
    # Write award results
    with open(os.path.join(args.outdir, f"{args.team_name}_award_results.txt"), "w", encoding="utf-8") as f:
        for r in award_results:
            f.write(str(r) + "\n")
    print(f"Wrote {len(team_results)} results for team '{args.team_name}' and {len(award_results)} award results to '{args.outdir}'")

if __name__ == "__main__":
    main()