import argparse
import sys
from app.emr_client import start_emr_job

def cli_main():
    parser = argparse.ArgumentParser(prog='emrrunner', description='Run the EMR API or start an EMR job')
    
    # Add arguments
    parser.add_argument('command', choices=['start'], help='Command to execute')
    parser.add_argument('--job', required=True, help='Job name')
    parser.add_argument('--step', required=True, help='Step name')
    parser.add_argument('--deploy-mode', choices=['client', 'cluster'], 
                       default='client', help='Spark deploy mode: client or cluster')

    try:
        args = parser.parse_args()
        
        if args.command == 'start':
            result = start_emr_job(args.job, args.step, args.deploy_mode)
            print(result)
            return 0
        return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(cli_main())