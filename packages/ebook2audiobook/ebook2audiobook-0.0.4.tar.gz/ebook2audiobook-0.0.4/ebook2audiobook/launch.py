import argparse
import subprocess
import sys
import os

def main():
    parser = argparse.ArgumentParser(
        description="Launch the ebook2audiobook app with parameters for conversion."
    )

    # Define all arguments as in app.py
    parser.add_argument("--share", type=bool, default=False)
    parser.add_argument("--headless", type=bool, default=False)
    parser.add_argument("--ebook", type=str)
    parser.add_argument("--voice", type=str)
    parser.add_argument("--language", type=str, default="en")
    parser.add_argument("--use_custom_model", type=bool, default=False)
    parser.add_argument("--custom_model", type=str)
    parser.add_argument("--custom_config", type=str)
    parser.add_argument("--custom_vocab", type=str)
    parser.add_argument("--custom_model_url", type=str)
    parser.add_argument("--temperature", type=float, default=0.65)
    parser.add_argument("--length_penalty", type=float, default=1.0)
    parser.add_argument("--repetition_penalty", type=float, default=2.0)
    parser.add_argument("--top_k", type=int, default=50)
    parser.add_argument("--top_p", type=float, default=0.8)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--enable_text_splitting", type=bool, default=False)

    args = parser.parse_args()

    # Dynamically locate app.py based on the current directory of launch.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "app.py")

    # Ensure that app.py exists at this path
    if not os.path.exists(app_path):
        print(f"Error: Could not find app.py at {app_path}")
        sys.exit(1)

    # Build the command to call app.py with arguments
    command = [sys.executable, app_path]  # Ensure app_path is used as a script

    # Append each argument if it's provided by the user
    if args.share is not None:
        command += ["--share", str(args.share)]
    if args.headless is not None:
        command += ["--headless", str(args.headless)]
    if args.ebook:
        command += ["--ebook", args.ebook]
    if args.voice:
        command += ["--voice", args.voice]
    if args.language:
        command += ["--language", args.language]
    if args.use_custom_model is not None:
        command += ["--use_custom_model", str(args.use_custom_model)]
    if args.custom_model:
        command += ["--custom_model", args.custom_model]
    if args.custom_config:
        command += ["--custom_config", args.custom_config]
    if args.custom_vocab:
        command += ["--custom_vocab", args.custom_vocab]
    if args.custom_model_url:
        command += ["--custom_model_url", args.custom_model_url]
    if args.temperature:
        command += ["--temperature", str(args.temperature)]
    if args.length_penalty:
        command += ["--length_penalty", str(args.length_penalty)]
    if args.repetition_penalty:
        command += ["--repetition_penalty", str(args.repetition_penalty)]
    if args.top_k:
        command += ["--top_k", str(args.top_k)]
    if args.top_p:
        command += ["--top_p", str(args.top_p)]
    if args.speed:
        command += ["--speed", str(args.speed)]
    if args.enable_text_splitting is not None:
        command += ["--enable_text_splitting", str(args.enable_text_splitting)]

    # Run app.py with all arguments
    subprocess.run(command)

if __name__ == "__main__":
    main()

