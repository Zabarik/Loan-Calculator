import math
import argparse
import sys


def get_annuity_payment(params):
    interest = params.interest / 100 / 12
    if params.periods is None:
        get_months(params.principal, params.payment, interest)
    if params.payment is None:
        get_monthly_annuity(params.principal, params.periods, interest)
    if params.principal is None:
        get_loan_principal(params.payment, params.periods, interest)


def get_months(principal, monthly_payment, interest):
    months = math.ceil(math.log(monthly_payment / (monthly_payment - interest * principal), 1 + interest))
    years = months // 12
    months = months - 12 * years
    if years != 0 and months != 0:
        print("It will take {} year{} and {} month{} to repay this loan!"
              .format(years, "s" if years > 1 else "", months, "s" if months > 1 else ""))
    elif months == 0:
        print("It will take {} year{} to repay this loan!"
              .format(years, "s" if years > 1 else ""))
    else:
        print("It will take {} month{} to repay this loan!".format(months, "s" if months > 1 else ""))
    print(f"\nOverpayment = {int(monthly_payment * (years * 12 - months) - principal)}")


def get_monthly_annuity(principal, months, interest):
    monthly_payment = principal * interest * (1 + interest) ** months / ((1 + interest) ** months - 1)
    print(f"Your monthly payment = {math.ceil(monthly_payment)}!")
    print(f"\nOverpayment = {int(math.ceil(monthly_payment) * months - principal)}")


def get_loan_principal(monthly_payment, months, interest):
    principal = monthly_payment / (interest * (1 + interest) ** months) * ((1 + interest) ** months - 1)
    print(f"Your loan principal = {round(principal)}!")
    print(f"\nOverpayment = {int(monthly_payment * months - principal)}")


def get_differentiated_payment(params):
    p = params.principal
    n = params.periods
    i = params.interest / 100 / 12
    sum_payments = 0
    for m in range(1, n + 1):
        payment = math.ceil(p / n + i * (p - p * (m - 1) / n))
        sum_payments += payment
        print(f"Month {m}: payment is {payment}")
    print(f"\nOverpayment = {int(sum_payments - p)}")


parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str, choices=["annuity", "diff"])
parser.add_argument("--principal", type=float)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)
parser.add_argument("--payment", type=float)
args = parser.parse_args()

if len(sys.argv) < 5 \
        or (not args.interest) \
        or (args.type == "diff" and args.payment) \
        or any([(param if param is not None else 1) < 0 for param in [args.principal, args.periods, args.interest, args.payment]]):
    print("Incorrect parameters")
    exit()

if args.type == "diff":
    get_differentiated_payment(args)
else:
    get_annuity_payment(args)
