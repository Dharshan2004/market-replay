from argparse import ArgumentParser
import collector

def main():
    parser = ArgumentParser(description="Market Replay CLI")
    parser.add_argument("--ticker", required=True, help="The ticker to capture data for")
    parser.add_argument("--time", required=True, help="Duration to capture data for")
    args = parser.parse_args()

    print(f"Capturing data for {args.ticker} for {args.time}s")
    
    # Start the collector with the parsed arguments
    collector.start_collector(args.ticker, args.time)

if __name__ == "__main__":
    main()