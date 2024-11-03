import argparse
from auto_loc import WebInspector

def main():
    parser = argparse.ArgumentParser(description="Run Web Inspector")
    parser.add_argument('--url', type=str, help="URL to inspect", required=True)
    args = parser.parse_args()

    inspector = WebInspector()
    inspector.start(args.url)
    inspector.quit()

if __name__ == "__main__":
    # e.g.: run-inspector --url "https://demoqa.com/automation-practice-form"
    main()
