import sys
import argparse
from calculator_helper import CalculatorHelper
import calculator_rest_service

parser = argparse.ArgumentParser(prog='ProgramName',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=('''Example of usage: python calculator.py --add 1 2'''))
parser.add_argument('-a', '--add',
                    nargs='+',
                    type=float,
                    required=False,
                    help='Add two numbers.'
                    )
parser.add_argument('-s', '--subtract',
                    nargs='+',
                    type=float,
                    required=False,
                    help='Subtract two numbers.'
                    )
parser.add_argument('-m', '--multiply',
                    nargs='+',
                    type=float,
                    required=False,
                    help='Multiply two numbers.'
                    )
parser.add_argument('-d', '--divide',
                    nargs='+',
                    type=float,
                    required=False,
                    help='Divide two numbers.'
                    )
parser.add_argument('-r', '--rest',
                    action='store_true',
                    help='Start the calculate REST service with default settings.'
                    )


args = parser.parse_args()

if not args.rest and len(sys.argv) != 4:
    print("Wrong number of arguments provided!\n")
    parser.print_help()
    sys.exit()

if (args.add):
    result = CalculatorHelper().add(args.add[0], args.add[1])
    print(f'{args.add[0]}+{args.add[1]}={result}')
elif (args.subtract):
    result = CalculatorHelper().subtract(args.subtract[0], args.subtract[1])
    print(f'{args.subtract[0]}-{args.subtract[1]}={result}')
elif (args.multiply):
    result = CalculatorHelper().multiply(args.multiply[0], args.multiply[1])
    print(f'{args.multiply[0]}*{args.multiply[1]}={result}')
elif (args.divide):
    result = CalculatorHelper().divide(args.divide[0], args.divide[1])
    print(f'{args.divide[0]}/{args.divide[1]}={result}')
elif (args.rest):
    calculator_rest_service.main(args)