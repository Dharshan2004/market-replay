import argparse
import collector
import metrics
import json
import os

def datacapture_command(args):
    print(f"Capturing data for {args.ticker} for {args.time}s")
    collector.start_collector(args.ticker, args.time)

def metrics_command(args):
    if not os.path.exists(args.filename):
        print(f"Error: File {args.filename} does not exist")
        return
    
    print(f"Analyzing metrics for {args.filename}")
    metrics.analyze_metrics(args.filename, args.epsilon)
    

def main():
    parser = argparse.ArgumentParser(
        description="Market Replay CLI",
        epilog="Examples:\n"
               "  python3 main.py datacapture --ticker btcusdt --time 10\n"
               "  python3 main.py metrics --filename data/data.ndjson",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Create subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # datacapture subcommand
    datacapture_parser = subparsers.add_parser('datacapture', help='Capture market data')
    datacapture_parser.add_argument('--ticker', '-t', required=True, help='Ticker symbol (e.g., btcusdt)')
    datacapture_parser.add_argument('--time', required=True, type=int, help='Duration to capture data (seconds)')
    datacapture_parser.set_defaults(func=datacapture_command)
    
    # metrics subcommand
    metrics_parser = subparsers.add_parser('metrics', help='Analyze captured data metrics')
    metrics_parser.add_argument('--filename', '-f', required=True, help='Path to the data file')
    metrics_parser.add_argument('--epsilon', '-e', required=False, type=float, help='Epsilon value for Ask≥Bid-ε check', default=1e-8)
    metrics_parser.set_defaults(func=metrics_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if a command was provided
    if not args.command:
        parser.print_help()
        return
    
    # Execute the appropriate command
    args.func(args)

if __name__ == "__main__":
    main()
